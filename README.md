# Walkthru inbox

Private inbox for customer moving walkthroughs.

- Customer page (separate public repo, GitHub Pages): customer enters name, zips, move date
  and packing answer, then records the walkthrough on the page or uploads a video.
- Uploads go to Cloudinary, tagged `walkthrough`, with the answers attached.
- `.github/workflows/fetch.yml` runs every 10 minutes and copies new uploads into `inbox/`.
- Claude processes each new folder with `PROCESSING.md`: inventory, clickable review page
  with video clips, and an email with the link.

Secrets this repo needs (Settings → Secrets and variables → Actions):
`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`.
