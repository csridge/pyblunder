# Pyblunder - A chess engine written in Python with the help of `python-chess` library
## 🧠 How to Play Against the Bot (on Windows using Arena)
### 1. Download and Set Up Arena

- Download Arena from http://www.playwitharena.de
- Extract the ZIP
- Open the folder and run `Arena.exe`
### 2. Clone This GitHub Repo

```bash
git clone https://github.com/csridge/pyblunder
cd pyblunder # Navigate to the repo
pip install -r requirements.txt # Install necessary packages
```
### 3. Adding and playing with the bot
- Open Arena. Select **Engines** on the top bar, then select **Install New Engine...**. After that, navigate to the GitHub repo, open the **dist** folder, and choose the **bot.exe** file.

- Press F11 to open the **Engine Management** tab, search for the bot you just added, right-click, select **Details**, select the type to **UCI**, and **press Apply** (you might need to wait for a bit) (Optional: Right click the bot name and choose "Select", though Arena should automatically select the bot).

- Now you can play with the bot.

## 🧠 How to Play Against the Bot (using Python) - for lazy people
If you don't even bother to install Python then, uhhhhhhhh, cmon
## 1. Install Python
- Install Python: https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe. Check the **Add Python to Path** box and continue with the default settings
Clone this GitHub repo:
```bash
git clone https://github.com/csridge/pyblunder
cd pyblunder # Navigate to the repo
pip install -r requirements.txt # Install necessary packages
```
- Run the bot with `python terminal_bot.py`
## How to sync latest update of the bot
Type this command: `git pull` (optional: reinstall packages using `pip install -r requirements.txt`)