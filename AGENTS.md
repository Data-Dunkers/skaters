# Project Instructions

## Facilitator guide source of truth

- `facilitators-guide/facilitators-guide.md` is the source of truth for the facilitator guide.
- `docs/fg.html` must always be generated from that Markdown file.
- Do not make content edits directly in `docs/fg.html`. Update the Markdown first, then regenerate the HTML page.
- Keep the full-resolution source images in `facilitators-guide/images/`. Because the site is published from `docs/`, copy the guide's referenced images into `docs/images/` and use `images/` paths in `docs/fg.html`.
- Keep the source PNGs at full resolution. Control their displayed size in the generated HTML instead of resizing the image files.
