# Processing a customer walkthrough (instructions for Claude)

Customers record a walkthrough on the Walkthru page. The video and their answers land in
Cloudinary, and the GitHub Action copies each one into `inbox/<folder>/` (`video.*` plus
`answers.json`). This file is the checklist for turning one into a review page.

1. `git pull`, then find every `inbox/*/answers.json` with `"status": "new"`.
2. For each one: `bash pipeline/prepare.sh inbox/<folder> /tmp/wt/<folder>`.
   That makes 1-per-second frames, contact sheets (`sheetNN.jpg`), a web-playable
   `walkthrough.mp4`, `img/poster.jpg` and `transcript.txt`.
3. Look at every contact sheet and read the transcript. If the video has no sound, it was
   probably recorded during a call; say so on the page (`"sound": "no"`).
4. Build the inventory with Top Nation's rules:
   - Use Granot's item names and preset cubic feet from `catalog/granot_items.txt`
     (`NAME|cf`). For anything not listed, use your own cubic-foot estimate and mark the
     line `"custom": true`.
   - Keep a preset unless it is egregiously wrong for what is in the video.
   - No plants. List them under `leftOff`.
   - Small loose items get no line item. Estimate their total cubic feet and turn that
     into a sensible box count: BOX, WARDROBE (16), BOX, LG PBO 18X18X24 (5),
     BOX, MED. PBO 18X16X18 (3), BOX, SM. PBO 12X12X18 (2), BOX, CHINA/DISH 18X18X28 (6).
     Small wall items such as a calendar or whiteboard are box items.
   - Anything the customer says is not going stays off and goes in `leftOff` with its time.
   - Do not sort into rooms. Pick a move size.
   - Flag the real judgment calls (2 to 5) with options; mark the one you chose
     `"current": true`.
5. Write `/tmp/wt/<folder>/spec.json` in the format of `review-kit/example-spec.json`.
   Leave out `job` and `pricing` until the file is in Granot. Include `packing` and
   `sound` from `answers.json`.
6. Copy every frame the spec references into `/tmp/wt/<folder>/img/`, then run
   `python3 review-kit/build.py /tmp/wt/<folder>`.
7. Publish `/tmp/wt/<folder>/index.html` with the Artifact tool, with `files` for
   `walkthrough.mp4` and each `img/*.jpg`. Title: "<First Last> Inventory Review". Icon: "box".
8. Email the link to cdubosque@yahoo.com. Subject: "Walkthrough ready: <First Last>".
   Body: name, route (zips), move date, packing answer, total cubic feet, the judgment
   calls in one line each, and the link.
9. In `answers.json` set `"status": "reviewed"`, `"review_url"` and `"reviewed_at"`.
   Commit and push.
