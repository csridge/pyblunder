# Pyblunder - A chess engine written in Python with the help of python-chess
## How to install and open Arena (for Windows users)
Install **Arena** from http://www.playwitharena.de, extract the ZIP folder, go to the Arena folder, then find and open the **Arena.exe** file.
## How to play against the bot
First of all, clone this GitHub repo:
`git clone https://github.com/csridge/pyblunder`

`cd pyblunder`

And install necessary packages: `pip install -r requirements.txt`
**It's recommended not to edit the repo.**

Open Arena. Select **Engines** on the top bar, then select **Install New Engine...**. After that, navigate to the GitHub repo, open the **dist** folder, and choose the **bot.exe** file.

Press F11 to open the **Engine Management** tab, search for the bot you just added, right-click, select **Details**, select the type to **UCI**, and **press Apply** (you might need to wait for a bit)
(Optional: Right click the bot name and choose "Select", though Arena should automatically select the bot)
Now you can play with the bot.

## How to sync latest update with the bot
Type this command: `git pull` (optional: reinstall packages using `pip install -r requirements.txt`)