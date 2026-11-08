# Work task mode (Christian, Nov 8 2026)

The scheduled task "Walkthru inbox check" (trig_01Y6Z6XBikM5HGsnoSUxLXTv) runs the walkthrough pipeline (PROCESSING.md) on a
self-scheduling loop, only while work task mode is on.

- "turn on work task mode": set `state/work-mode.json` `"on": true` (+ `changed_at`), commit and
  push, then fire the scheduled task "Walkthru inbox check" right away (list_triggers to find it,
  then fire_trigger). Each run then schedules the next one itself.
- "turn off work task mode": set `"on": false`, commit and push, then update the scheduled task
  "Walkthru inbox check" to `enabled: false` so no queued run fires.
- Interval: 1 minute while any walkthrough is `awaiting_customer`, otherwise 5 minutes.
- No backup task: if a run crashes or hits a usage limit, the loop stops until he turns it on again.
