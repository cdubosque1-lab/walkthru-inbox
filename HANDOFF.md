# HANDOFF: starting this work in a brand-new chat

Read this first, then PROCESSING.md (rules + flow) and WORK_MODE.md.

## Setup in a new session
1. Clone both repos: cdubosque1-lab/walkthru-inbox (private, this one) and cdubosque1-lab/walkthru (public customer page). Use add_repo, then git clone.
2. Scratchpad: `S=<your scratchpad>`; prepare a video with
   `ASR_DIR=$S/asr bash pipeline/prepare.sh inbox/<folder> $S/wt/<name>` (installs sherpa-onnx + whisper by itself; if the model download is blocked, the transcript step is skipped, so ask Christian to attach nothing, just note it).
3. Generator template: `examples/mk_snyder.py <workdir> <answers.json>` (writes spec.json + img/); then `python3 review-kit/build.py <workdir>`. Other examples/ show older variants. snyder_doc.json is a sample db doc.
4. Chrome: use Claude in Chrome (tabs_context_mcp first). Granot admin tab = the one on the Granot admin page; load tools with ToolSearch (see claude-in-chrome skill). browser_batch needs `{name, input}` actions.
5. Loop: only when Christian says "work task mode on" (state/work-mode.json {"on":true}). Tick = send_later +1 min FIRST, then ReadNotifications, pull, dispatch fetch.yml, sleep ~22s, pull, check `"status": "new"`, callbacks with `"emailed": false`, db docs "approved". "off" stops it.

## Granot click guide (screen coordinates on the 1-tab layout; re-verify with a screenshot)
- Admin tab: New Estimate (292,287) opens a NEW tab. Local/Long Distance link (390,77).
- Find existing job: type job no. (e.g. T4120051) in admin Search box (392,234), Search (578,234); job opens in a new tab on the Charges page. Entry Form tab has Phone 1/2/3, Mobile, Fax, Email, Proxy (email), Job No., Move date. Charges page has Follow Up date/time.
- Estimate form fields: customer (326,103); from address (326,128), city (266,228), state (383,228), zip (252,253); phone (311,279); email (311,330); to address (672,128), city (612,228), state (730,228), zip (598,253); date (370,405) (typing MM/DD/YYYY opens a picker, click the highlighted day); lead source (430,437) click, type "refer", Enter (may need 2 tries); move size via form_input on the select (e.g. "Studio"); Continue to Inventory (356,535).
- Inventory page: `filterINV('all')`; build name->index map from `.querySelectorAll('font')` onclick `/alterQty\((\d+),\s*\+?1\)/` (393 items); `alterQty(idx,n)` adds; custom lines via #NEWITEM / #NEWVOLUME / #NEWQTY + `addNewItem()`; `clearItems()` (set `window.confirm=()=>true` first) to wipe before a re-entry; Submit (87,75). Verify total cf by zooming [0,50,958,110]. Long-distance bills a 300 cf minimum.
- javascript_tool only returns the last expression; trick: set document.title and read it from the tab context.
- Charges page, Packing Materials link, then Materials page qty boxes (scroll to top, use coordinates not refs): small box (534,108), dish/china (534,130), linen/medium (534,174), medium/large (534,196). Submit via find ref, scroll_to, click. Prices: small $6, dish $16, medium $9, large $10, wardrobe $16.50.
- Granot box names: BOX SM PBO 12X12X18 (2 cf), MED 18X16X18 (3), LG 18X18X24 (5), CHINA/DISH 18X18X28 (6), WARDROBE (16).
- Duplicate/canceled email warning: use random 10-char letters+numbers @gmail.com. No email: random 8 letters @gmail.com.

## Artifact / db
Publish review with the Artifact tool: `files` map + `root`, capabilities `{"db": {}, "mcp": {"servers": [{"server": "Claude Code Remote", "tools": ["fire_trigger"]}]}}`. ArtifactData `set` with `file_path` JSON writes the granot/request doc (status entered / approved).

## Email
Gmail connector sends from veritascompound@gmail.com (Christian wants cdubosque1@gmail.com; unresolved, parked). Send ONLY to cdubosque@yahoo.com.

## Commits
Trailers: Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com> and Claude-Session line from the system reminder.
