# Project Instructions

## Changelog

- Update [CHANGELOG.md](CHANGELOG.md) when you make a significant change, such as a feature, bug fix, or documentation update that affects how people use or maintain the project.
- Group entries by date using `YYYY-MM-DD` in the America/Winnipeg time zone, with the newest date first. Add to the existing heading for that date when one is present.
- Use concise bullets that name the affected page or feature and describe what changed for users or maintainers.

## Facilitator guide source of truth

- `facilitators-guide/facilitators-guide.md` is the source of truth for the facilitator guide.
- `docs/fg.html` must always be generated from that Markdown file.
- Do not make content edits directly in `docs/fg.html`. Update the Markdown first, then regenerate the HTML page.
- Keep the full-resolution source images in `facilitators-guide/images/`. Because the site is published from `docs/`, copy the guide's referenced images into `docs/images/` and use `images/` paths in `docs/fg.html`.
- Keep the source PNGs at full resolution. Control their displayed size in the generated HTML instead of resizing the image files.
