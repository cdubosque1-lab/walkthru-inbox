"""Build a per-job inventory review page from a spec.json.

Usage: python3 build.py <job_folder>
The job folder holds spec.json, walkthrough.mp4 and img/*.jpg; index.html is written there.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    folder = sys.argv[1]
    with open(os.path.join(folder, "spec.json"), encoding="utf-8") as f:
        spec = json.load(f)
    spec["items"].sort(key=lambda i: i["t"])
    spec["boxes"].sort(key=lambda i: i["t"])
    spec["flags"].sort(key=lambda i: i["t"])
    if any(i.get("room") for i in spec["items"] + spec["boxes"]):
        first = {}
        for i in spec["items"] + spec["boxes"]:
            r = i.get("room", "Other")
            i["room"] = r
            first[r] = min(first.get(r, 1e9), i["t"])
        spec["rooms"] = sorted(first, key=lambda r: first[r])
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        html = f.read()
    data = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__TITLE__", spec["title"]).replace("__DATA_JSON__", data)
    out = os.path.join(folder, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    items = spec["items"] + spec["boxes"]
    total = sum(i["cf"] * i["qty"] for i in items)
    missing = [i["img"] for i in items + spec["flags"] + spec["leftOff"] if not os.path.exists(os.path.join(folder, i["img"]))]
    print(f"wrote {out}: {len(items)} lines, {total} cf, missing images: {missing or 'none'}")


if __name__ == "__main__":
    main()
