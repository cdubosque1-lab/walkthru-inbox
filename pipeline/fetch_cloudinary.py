"""Copy new customer walkthroughs from Cloudinary into inbox/.

Runs inside GitHub Actions. Needs CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY and
CLOUDINARY_API_SECRET as repository secrets. Videos are found by the "walkthrough"
tag the customer page adds; the customer's answers come from the upload's context.
"""
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request

CLOUD = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
KEY = os.environ.get("CLOUDINARY_API_KEY", "").strip()
SECRET = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
STATE = "state/seen.json"
MAX_BYTES = 99 * 1024 * 1024  # GitHub rejects files over 100 MB


def api(path: str, params: dict) -> dict:
    url = f"https://api.cloudinary.com/v1_1/{CLOUD}/{path}?" + urllib.parse.urlencode(params)
    token = base64.b64encode(f"{KEY}:{SECRET}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + token})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> None:
    if not (CLOUD and KEY and SECRET):
        sys.exit("Missing Cloudinary secrets (CLOUDINARY_CLOUD_NAME / _API_KEY / _API_SECRET).")
    seen = set(json.load(open(STATE))) if os.path.exists(STATE) else set()
    resources, cursor = [], None
    while True:
        params = {"context": "true", "max_results": 100}
        if cursor:
            params["next_cursor"] = cursor
        page = api("resources/video/tags/walkthrough", params)
        resources += page.get("resources", [])
        cursor = page.get("next_cursor")
        if not cursor:
            break

    added = 0
    for r in sorted(resources, key=lambda x: x.get("created_at", "")):
        pid = r["public_id"]
        if pid in seen:
            continue
        ctx = (r.get("context") or {}).get("custom", {})
        name = f"{ctx.get('first', '')} {ctx.get('last', '')}".strip() or "customer"
        stamp = r.get("created_at", "")[:16].replace(":", "")
        slug = re.sub(r"[^a-z0-9]+", "-", f"{stamp} {name}".lower()).strip("-")
        folder = os.path.join("inbox", slug)
        os.makedirs(folder, exist_ok=True)
        ext = r.get("format") or "mp4"
        meta = {
            "status": "new",
            "public_id": pid,
            "created_at": r.get("created_at"),
            "bytes": r.get("bytes"),
            "format": ext,
            "width": r.get("width"),
            "height": r.get("height"),
            "answers": ctx,
            "video_file": f"video.{ext}",
        }
        if (r.get("bytes") or 0) > MAX_BYTES:
            meta["status"] = "too_big"
            meta["note"] = "Over 99 MB, so it stays in Cloudinary. Download it there."
        else:
            urllib.request.urlretrieve(r["secure_url"], os.path.join(folder, f"video.{ext}"))
        with open(os.path.join(folder, "answers.json"), "w") as f:
            json.dump(meta, f, indent=2)
        seen.add(pid)
        added += 1
        print(f"added {folder}")

    # Customers' answers to the judgment-call questions (tiny images tagged walkthrough_answers).
    os.makedirs("state/calls", exist_ok=True)
    try:
        page = api("resources/image/tags/walkthrough_answers", {"context": "true", "max_results": 100})
        for r in page.get("resources", []):
            ctx = (r.get("context") or {}).get("custom", {})
            uid = re.sub(r"[^A-Za-z0-9]", "", ctx.get("uid", ""))
            if not uid:
                continue
            path = os.path.join("state", "calls", uid + ".json")
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump({"answers": ctx, "created_at": r.get("created_at")}, f, indent=2)
                print(f"customer answers for {uid}")
    except Exception as e:  # never block video fetching on this
        print("answers fetch failed:", e)

    # Customers who tapped "Not right now" and picked a callback time.
    os.makedirs("state/callbacks", exist_ok=True)
    try:
        page = api("resources/image/tags/walkthrough_callback", {"context": "true", "max_results": 100})
        for r in page.get("resources", []):
            ctx = (r.get("context") or {}).get("custom", {})
            uid = re.sub(r"[^A-Za-z0-9]", "", ctx.get("uid", ""))
            if not uid:
                continue
            path = os.path.join("state", "callbacks", r["public_id"].replace("/", "_") + ".json")
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump({"callback": ctx, "created_at": r.get("created_at"), "emailed": False}, f, indent=2)
                print(f"callback request for {uid}")
    except Exception as e:
        print("callback fetch failed:", e)

    os.makedirs("state", exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(sorted(seen), f, indent=2)
    print(f"new walkthroughs: {added}")


if __name__ == "__main__":
    main()
