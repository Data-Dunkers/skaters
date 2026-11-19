## 2026-11-19T10:56:30-0500

Goal: Remove unnecessary source attribution from the facilitator guide.

Prompt summary: Keep the confirmed explanation of 43 but remove the citation references from both the Markdown guide and the web page.

Hostname: m4-mini
Active agent: Codex
Technical context: Updated `facilitators-guide/facilitators-guide.md` and `docs/fg.html`.

## 2026-11-19T10:55:30-0500

Goal: Make facilitator-guide slide images visible on the site.

Prompt summary: Copy the full-resolution guide images into the published `docs/images/` directory and update `docs/fg.html` to use site-local image paths.

Hostname: m4-mini
Active agent: Codex
Technical context: The site publishes from `docs/`, so assets outside that directory were not reachable by the web page.

## 2026-11-19T10:54:30-0500

Goal: Document the facilitator-guide source-of-truth workflow.

Prompt summary: Create a root `AGENTS.md` explaining that `docs/fg.html` must always be generated from `facilitators-guide/facilitators-guide.md`.

Hostname: m4-mini
Active agent: Codex
Technical context: Added source-of-truth and image-handling instructions for the facilitator guide.

## 2026-11-19T10:53:30-0500

Goal: Place the facilitator guide web page in the site directory.

Prompt summary: Move `fg.html` from the project root into `docs/` and update its relative image paths so it renders correctly on the site.

Hostname: m4-mini
Active agent: Codex
Technical context: The page is now `docs/fg.html` and references images through `../facilitators-guide/images/`.

## 2026-11-19T10:52:56-0500

Goal: Convert the facilitator guide into a root-level web page.

Prompt summary: Create `fg.html` in the project root, preserving the compact slide-focused guide and its linked images.

Hostname: m4-mini
Active agent: Codex
Technical context: Added a standalone responsive HTML page with slide images displayed at 400px wide.

## 2026-11-19T10:51:30-0500

Goal: Reduce the facilitator-guide image display size.

Prompt summary: Decrease the embedded slide display width from 800px to 400px while keeping the full-resolution source PNGs unchanged.

Hostname: m4-mini
Active agent: Codex
Technical context: Updated HTML image widths in `facilitators-guide/facilitators-guide.md` only.

## 2026-11-19T10:50:30-0500

Goal: Preserve full-size source images while reducing their guide display size.

Prompt summary: Restore the slide PNGs to full resolution and set the facilitator guide to display them at 50% width instead of modifying the source image files.

Hostname: m4-mini
Active agent: Codex
Technical context: Restore slide images to 1600x900 and use 800px HTML image widths in `facilitators-guide/facilitators-guide.md`.

## 2026-11-19T10:49:30-0500

Goal: Clarify the student player-ID requirement.

Prompt summary: Update the facilitator and educator guides to state that students must use their actual initials plus two digits, and must keep the same player ID throughout the session because it is needed to identify and correct data-entry mistakes.

Hostname: m4-mini
Active agent: Codex
Technical context: Revised player-ID instructions in both Markdown guides.

## 2026-11-19T10:48:30-0500

Goal: Confirm the PS43 explanation and correct a facilitator name.

Prompt summary: Verify that 43 represents four male and three female family members, update the guide with the confirmed family breakdown, and spell Karl's name with a K.

Hostname: m4-mini
Active agent: Codex
Technical context: Updated the slide 2 notes in `facilitators-guide/facilitators-guide.md`.

## 2026-11-19T10:47:47-0500

Goal: Reduce facilitator-guide image sizes.

Prompt summary: Resize the embedded slide PNGs to 50% of their original dimensions while preserving filenames and Markdown links.

Hostname: m4-mini
Active agent: Codex
Technical context: Slide images in `facilitators-guide/images` were resized from 1600x900 to 800x450.

## 2026-11-19T10:47:22-0500

Goal: Make the facilitator guide compact and slide-centred.

Prompt summary: Reduce redundancy, move useful setup and facilitation details into the relevant slide sections, and keep the guide short enough for facilitators to use during a session.

Hostname: m4-mini
Active agent: Codex
Technical context: Condense `facilitators-guide/facilitators-guide.md` while retaining the exported slide images and essential educator-guide guidance.

## 2026-11-19T10:42:30-0500

Goal: Clarify the event-key convention.

Prompt summary: Update the facilitator guide to explain that the event key usually comes from the school name, using Miskooseepi School and `MS` as the example.

Hostname: m4-mini
Active agent: Codex
Technical context: Revise the quick-start setup note in `facilitators-guide/facilitators-guide.md`.

## 2026-11-19T10:41:22-0500

Goal: Make the facilitator guide a fast session reference.

Prompt summary: Review the root educator guide and add useful, concise setup, workflow, data-collection, analysis, accessibility, and facilitation guidance to the facilitator guide.

Hostname: m4-mini
Active agent: Codex
Technical context: Update the Markdown guide in `facilitators-guide` using `EDUCATOR-GUIDE.md` as the source.

## 2026-11-19T10:39:43-0500

Goal: Create a facilitator guide from a Google Slides presentation and transcript.

Prompt summary: Build `facilitators guide.md` in the `facilitators-guide` folder, incorporate the relevant slide PNGs according to the supplied transcript, and edit the transcript into clear facilitator-facing language rather than reproducing it verbatim.

Hostname: m4-mini
Active agent: Codex
Technical context: Source presentation contains the Data Skaters AI Performance Lab introduction and exported slide images are stored in `facilitators-guide/images`.
