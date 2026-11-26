# Changelog

## 2026-11-26

- **Maintenance** adds a password prompt for development and loads event nicknames after the page is unlocked.

## 2026-11-25

- **Maintenance** adds a read-only player lookup with an alphabetical nickname dropdown populated from the selected event’s photo, traits, shooting, and Rocket League submissions.
- **Visualizations** averages all bar chart metrics per student so groups of different sizes can be compared. The Python examples use the same aggregation.
- **Collected Data** shows the Rocket League column and checks for Rocket League submissions only after Rocket League data has been collected.
- **Collected Data** and **Visualizations** move their headings and content higher on the page while keeping the Home button clear on narrow screens.

## 2026-11-24

- **Visualizations** collapses each chart’s Python example by default. Open **Python code** to view it.
- **Visualizations** averages player shot percentages for each bar and displays them on a 0–100% axis.
- **Collected Data** and **Nicknames** show a small countdown bar while auto-refresh is on. The Collected Data checkbox now displays its existing 30-second interval.
- **Collected Data** remembers the last sort column and direction and restores them after page reloads, auto-refreshes, and filter changes.
- **Nicknames** now remembers the last **Select All** or **Clear All** choice in the browser. Photos are shown by default, and the on-page hint explains that tapping a nickname shows or hides its photo.
- **Nicknames** has an optional one-minute auto-refresh. The browser remembers whether it is enabled, and every refresh reapplies the saved photo selection to the latest records.
- **Today's Top Ten** now sends users to Data Skaters Home when they click **Home** or visit without an event key.
