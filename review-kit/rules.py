"""Helpers for the Nov 8 redesign (packing/storage/TV/mirror/picture questions, rapport cards).

Used by the per-walkthrough generator (see PROCESSING.md, "V2 FLOW")."""

PACKING = {
    "we_pack": "Yes, wants us to supply and pack all boxes",
    "self": "No, will supply and pack own boxes",
    "some": "Will do some, wants movers to do some",
    "unsure": "Not sure yet",
}
STORAGE = {"yes": "Yes", "no": "No", "maybe": "Maybe"}

INTRO = ("We always take care of disassembly and reassembly of standard furniture, full blanket, pad and "
         "shrink wrapping of all furniture, and all the loading and unloading, at no extra charge. "
         "Just a few quick questions about packing:")


def packing_label(form):
    return PACKING.get(form.get("packing", ""), form.get("packing", ""))


def judgment_questions_for_items(item_names):
    """Triggered questions: TVs, mirrors, pictures. item_names = Granot names of the items in the inventory."""
    up = [n.upper() for n in item_names]
    qs = []
    if any("T.V." in n or n.startswith("TV") for n in up):
        qs.append({"id": "tvbox", "text": "We require TVs to be in TV boxes. Would you like us to supply them for you (a little extra cost), or will you supply your own TV boxes?",
                   "options": [{"key": "we", "label": "Please supply TV boxes for me"}, {"key": "self", "label": "I'll supply my own TV boxes"}]})
    if any("MIRROR" in n for n in up):
        qs.append({"id": "mirror", "text": "Would you like us to pack up your mirror(s), or will you do that yourself?",
                   "options": [{"key": "we", "label": "Please pack them for me"}, {"key": "self", "label": "I'll do that myself"}]})
    if any("PICTURE" in n or "ART" in n for n in up):
        qs.append({"id": "pictures", "text": "Would you like us to pack up your pictures and artwork, or will you do that yourself?",
                   "options": [{"key": "we", "label": "Please pack them for me"}, {"key": "self", "label": "I'll do that myself"}]})
    return qs


def talk_cards(form, old=None):
    """Rapport cards for the review page. old = what Granot had before (name/phone/email) when a job number was used."""
    c = []
    p = form.get("packing")
    if p == "some":
        c.append({"title": "Packing: some by customer, some by movers",
                  "text": "Ask which rooms or items they want packed (kitchen? books? fragile pieces?) and which they will do themselves."})
    if p == "unsure":
        c.append({"title": "Packing: not sure yet",
                  "text": "Walk them through the options: full packing, just fragile and kitchen items, or all self-pack. Good moment to build rapport."})
    st = form.get("storage")
    if st in ("yes", "maybe"):
        c.append({"title": "Storage: " + STORAGE[st] + (" (" + form["storage_len"] + ")" if form.get("storage_len") else ""),
                  "text": "30 days free with free redelivery, then $0.50 per cubic foot. Quote the monthly rate from the inventory total."})
    old = old or {}
    full = (form.get("first", "") + " " + form.get("last", "")).strip()
    if old.get("name") and old["name"].strip().lower() != full.lower():
        c.append({"title": "Name changed", "text": "Granot had \"" + old["name"] + "\"; the customer typed \"" + full + "\". Good to confirm who is on the move."})
    for k, label in (("phone", "Phone"), ("email", "Email")):
        if old.get(k) and form.get(k) and old[k] != form[k]:
            c.append({"title": label + " changed", "text": "Customer typed " + form[k] + " (now primary). Previously in Granot: " + old[k] + " (kept as secondary)."})
    return c
