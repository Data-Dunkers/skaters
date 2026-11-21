# Data Skaters

Resources and pages for Data Skaters

## Creating player cards

Player cards are generated from the data collected during an event.

1. Open the [Data Skaters site](https://datadunkers.ca/skaters) and enter the event key used for the session. The event key connects the photos, traits, shot results, and Rocket League results for that event.
2. Complete the data collection forms. Each student should use the same four-character player ID all day; the first two characters must be the student's actual initials, followed by two digits (for example, `PS43`).
3. Open the [Player Card Creator](https://datadunkers.ca/skaters/card-creator/index.html). It retrieves the event's records, uses the latest photo for each player, calculates shot percentages and data-based archetypes, and adds the collected measurements and results to each card.
4. Review the generated cards. Each card can be downloaded as a PNG, or all cards can be exported as a letter-size PDF or a 4×6 PDF for printing, cutting, folding, and placing in card protectors.

To test the page with a smaller set of cards, use the [testing view](https://datadunkers.ca/skaters/card-creator/index.html?testing=true). To generate one player's card, add a `nickname` parameter, such as `?nickname=PS43`.

## Setting up a Data Skaters server on a Windows computer:

* Press the Windows key and type `PowerShell`
* Right-click Windows PowerSheell and choose **Run as administrator**
* Copy the following line and paste it into the PowerShell:

`iwr -useb https://raw.githubusercontent.com/Data-Dunkers/skaters/refs/heads/main/setup/windows-setup.ps1 | iex`

* Press the Enter key to run the script.

## Setting up a Data Skaters server on a Linux computer:

`curl -fsSL https://raw.githubusercontent.com/Data-Dunkers/skaters/refs/heads/main/setup/linux-setup.sh | sudo bash`
