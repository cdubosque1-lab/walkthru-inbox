## LIVE LOOP (Nov 8, supersedes the cloud scheduled task)
The cloud scheduled task "Walkthru inbox check" is DISABLED on purpose: a cloud run has no access to
Christian's Chrome (Granot) and cannot push to the public walkthru repo, so it produced defaults-only
reviews and never sent the customer questions. Everything runs in the interactive session instead,
driven by a send_later loop (every 1 minute) that only continues while state/work-mode.json "on" is true.
Each tick, FIRST re-book the next tick (send_later, 1 minute), then:
1. git pull both repos; dispatch fetch.yml (gh api -X POST .../fetch.yml/dispatches -f ref=main); wait ~30s; pull.
2. NEW upload (status "new"): claim it at once (status processing, push), then prepare.sh, watch the video, build
   the inventory, write results/<uid>.json with the judgment questions (walkthru repo), push, status awaiting_customer.
   Target: questions on the customer's screen within a few minutes of upload.
3. ANSWERS arrive (state/calls/<uid>.json): in ONE pass, build + publish the review page, then enter Granot
   (flat list, packing=No -> boxes into Packing Materials), set the db doc to entered, then set "done": true in the
   customer's results file (this is what takes the bar to 100% and shows the call button) and send ONE email.
   Review page may be published (and its link emailed) in parallel with the Granot entry; done:true only AFTER Granot is entered.
4. db doc "approved" (Update Granot version): re-enter into the same job, short "Granot updated" email.
Never send Granot emails/texts, never e-sign, never type passwords, email only cdubosque@yahoo.com.

# Processing customer walkthroughs (instructions for Claude)

Customers record a walkthrough on the Walkthru page. The video and their answers land in
Cloudinary, and the GitHub Action copies each one into `inbox/<folder>/` (`video.*` plus
`answers.json`). Each walkthrough moves through these statuses in its `answers.json`:

`new` → `processing` (claimed) → `awaiting_customer` (judgment-call questions sent to the
customer's screen) → `reviewed` (review page live, waiting for the rep) → `entered` (in Granot).
`error` means something needs Christian.


## NEW FLOW (Christian, Nov 8, overrides the approval steps below)

As soon as the customer's answers arrive (`state/calls/<uid>.json`), do all of this in one go,
without waiting for any button:
1. Apply the answers, build and publish the review page (Part A steps 6b to 8).
2. Immediately enter the inventory in Granot (Part B steps 3 to 5b, new job).
3. Write the page's database doc with ArtifactData `set` (collection `granot`, doc_id `request`):
   `status: "entered"`, `job`, `entered_at`, `customer`, `move_size`, `move_date`, `route`,
   `lines`, `total_cf`, `est_lbs`, `box_count`, `open_checks: 0`, `notes: ""`.
4. Part B step 6c: set `"done": true` in the customer's results file so their bar hits 100% and the call-in pop-up shows.
5. Send ONE email to cdubosque@yahoo.com: subject "Walkthrough ready and entered in Granot: <name>, job <number>".
   Body: name, phone, route, move date, bedrooms, packing answer, total cf and price, one line per
   judgment call with the customer's answer, anything unusual, and the review page link. Tell him
   he can go over the judgment calls with the customer on the call and press **Update Granot version**.
6. Set `answers.json` `status: "entered"` plus `review_url`, `granot_job`, `reviewed_at`, `granot_entered_at`. Commit and push.
Later, when the page's doc reads `status: "approved"` (he pressed Update Granot version), re-enter
the changed inventory into the SAME job (Part B step 4 with `granot_job`, `clearItems()` first, redo packing
materials for packing=No), set the doc back to `entered`, and email a short "Granot updated" note.
If Granot is logged out or Chrome is unavailable, still email the review link and say what is waiting.

## A. Build the review page for each `new` walkthrough

1. `git pull`, then find every `inbox/*/answers.json` with `"status": "new"`.
2. Claim it before doing anything else: set `"status": "processing"` and `"claimed_at"`,
   commit and push. If the push is rejected, `git pull --rebase`; if it is no longer
   `new`, someone else has it, so skip it.
3. `bash pipeline/prepare.sh inbox/<folder> /tmp/wt/<folder>` makes 1-per-second frames,
   contact sheets (`sheetNN.jpg`), a web-playable `walkthrough.mp4`, `img/poster.jpg`
   and `transcript.txt`.
4. Look at every contact sheet and read the transcript. If the video has no sound it was
   probably recorded during a call (`"sound": "no"`).
5. Build the inventory with Top Nation's rules:
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
   - SORT BY ROOM, REVIEW PAGE ONLY (Christian, Nov 7: rooms on the review page, NOT in
     Granot). Give every item, box line and left-off note a `"room"` (Bathroom, Closet,
     Bedroom, Kitchen...). Order rooms by when each first appears in the video. Boxes are
     split by room too (e.g. Kitchen: china boxes). review-kit/build.py groups the page by
     room automatically. Move size comes from the customer's bedrooms answer
     (`answers.bedrooms`); use your judgment only if it clearly doesn't match the video.
   - Flag the real judgment calls (2 to 5) with options; mark the one you chose
     `"current": true`.
6. Write `/tmp/wt/<folder>/spec.json` in the format of `review-kit/example-spec.json`.
   Leave out `job` and `pricing`. Include `packing` and `sound` from `answers.json`.
   If the scheduled task "Walkthru: Input into Granot wake-up" exists and is enabled
   (list_triggers), add `"wakeTrigger": "<its trig_ id>"` so the button wakes Claude
   the moment it is pressed.
6b. **Ask the customer the judgment calls first.** The customer's page is sitting on an
   "Analyzing video" bar and is polling for a file. For every flag the customer can answer
   (sectional size, coffee table size, "is this going?" for washer and dryer, a bike, etc.;
   never cubic feet, never anything about price), add to the flag
   `"ask": {"text": "plain question", "options": [{"key": <same key as the flag option>, "label": "2-piece"}...]}`.
   Then write `/home/claude/walkthru/results/<uid>.json` (`uid` is in `answers.json` under
   `answers.uid`) as `{"questions": [{"id": <flag id>, "text": ..., "options": [...]}]}`,
   commit and push that repo (it is the public customer page; put nothing personal in the
   file). The customer's bar then hits 100% and shows the questions. Set `answers.json`
   `"status": "awaiting_customer"` plus `"questions_at"`, commit and push the inbox repo,
   keep the work folder, and stop. Do not publish or email yet.
   FAST PATH (Christian, Nov 7): while any walkthrough is `awaiting_customer`, check every 1 minute (not 5) and build/publish the review page the moment the customer's answers arrive. Do not wait for the next 5-minute check.
   On later checks, for each `awaiting_customer`: if `state/calls/<uid>.json` exists, read
   the customer's `q_<flag id>` answers, apply them (set item names and cf from the chosen
   option for single-item flags; set qtys yourself for multi-item flags like washer and
   dryer), mark the chosen option `"current": true`, and put "Customer answered: X" at the
   start of that flag's `detail`. If 20 minutes pass with no answer, go ahead with your
   defaults and note "Customer didn't answer" on those flags. Then continue below.
7. Copy every frame the spec references into `/tmp/wt/<folder>/img/`, then run
   `python3 review-kit/build.py /tmp/wt/<folder>`.
8. Publish `/tmp/wt/<folder>/index.html` with the Artifact tool, with
   `capabilities: {"db": {}}` (the Input into Granot button needs it) and `files` for
   `walkthrough.mp4` and each `img/*.jpg`. Title "<First Last> Inventory Review", icon "box".
   When the spec has `wakeTrigger`, use
   `capabilities: {"db": {}, "mcp": {"servers": [{"server": "Claude Code Remote", "tools": ["fire_trigger"]}]}}`.
9. Email the link to cdubosque@yahoo.com. Subject: "Walkthrough ready: <First Last>".
   Body: name, phone, route (zips), move date, packing answer, total cubic feet and box
   count, one line per judgment call, and the link.
10. In `answers.json` set `"status": "reviewed"`, `"review_url"` and `"reviewed_at"`.
    Commit and push.

## B. Enter approved inventories into Granot

The review page's **Input into Granot** button is the rep's approval. It writes the
approved inventory to the page's database: collection `granot`, document `request`,
with `status: "approved"`, `approved_at`, `lines` (name, cf, qty, custom, box, room),
`total_cf`, `box_count`, `notes`.

1. For every `answers.json` with status `reviewed` or `entered`, read that document with
   ArtifactData (`action: "get"`, `url`: the review_url, `collection: "granot"`,
   `doc_id: "request"`). Act only when its status is `approved`.
2. This needs Claude in Chrome with Christian's Granot login. If those browser tools
   aren't available, don't try: email cdubosque@yahoo.com that "<name>" is approved and
   waiting for Granot entry, and stop.
3. Open Granot (https://puma.hellomoving.com/topnatrelo/admin.htm). If it asks for a
   login, email Christian to log in and stop. Never type passwords.
4. If `answers.json` has `granot_job`, open that job and go to Inventory. Otherwise search
   the Salesperson Menu for the customer's name and phone; if a matching open estimate
   exists, use it. If not, New Estimate → Local / Long Distance → Entry Form:
   - customer name, Phone 1 (from answers), email (theirs; if none, a random 8-letter
     combination @gmail.com; if Granot says the email already has an estimate, a random
     10-character mix of letters and numbers @gmail.com);
   - origin and destination street address, city, state and zip (all in `answers`:
     from_addr/from_city/from_state/from_zip and to_*);
   - move date; lead source REFERRAL only if blank; move size from the review spec;
   - Continue to Inventory.
5. Inventory: enter it as one flat list, NOT by room (Christian changed his mind Nov 7; rooms are only on the review page). Don't touch Granot's room buttons. Run `filterINV('all')`, map each Granot item name to its `alterQty(index, +1)`
   index from the item rows, and if you are updating a job that already has items, call
   `clearItems()` first. Add each approved line with `alterQty(index, n)`; add custom
   lines with the NEWITEM / NEWVOLUME / NEWQTY fields and the Add New Item button. Check
   the page total matches `total_cf`, then Submit (`submitToCharges()`).
5b. PACKING MATERIALS (Christian, Nov 7). If `answers.packing` is "No" (customer wants packing
   help), also add every box on the inventory list (same box types and counts) to the
   file's Packing Materials section on the Charges page, then check the price. Only for
   "No"; for "Yes" or "Some" leave Packing Materials alone (mention "Some" in the email
   so Christian can decide). Never email or send anything from Granot.
6. Read the job number from the Charges page. Update the page's document with ArtifactData
   (`update`, pinned with `if_version`): `status: "entered"`, `job`, `entered_at`.
   In `answers.json` set `status: "entered"`, `granot_job`, `granot_entered_at`; commit
   and push. Email Christian: "Entered in Granot: <name>, job <number>, <cf> cf, <price>".
6c. **Tell the customer's screen it is done.** Right after the job is in Granot, open
   `/home/claude/walkthru/results/<uid>.json`, add `"done": true`, commit and push that repo.
   The customer's loading bar then jumps to 100% and shows the "Call in now for an additional
   $300 off" pop-up. (If a walkthrough had no questions, create the file as `{"done": true}`.
   Do this only after the entry succeeded and the Charges page shows the job.)
7. If anything fails, set the document's `status: "error"` with a short `message`, and
   email Christian what happened.

Never send Granot emails or e-sign documents, and never email anyone but
cdubosque@yahoo.com.
