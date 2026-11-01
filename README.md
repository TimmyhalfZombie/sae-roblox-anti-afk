# Roblox Anti-AFK

Roblox kicks you out of a game if you don't press anything for 20 minutes.
This little program stops that from happening, so you can stay in the game while you're away.

**How it works:** every 4 to 8 minutes, it quickly switches to Roblox, zooms the camera
in and out (the **I** and **O** keys), then switches back to whatever you were doing.
It takes about one second.

It only presses those two keys. It never touches your Roblox account or password.

It only works on **Windows** computers (not Mac, phone, tablet or Xbox).

> **Kids:** ask a parent or guardian before installing anything on the computer.

---

## Part 1: Set it up (only once)

### Step 1: Install Python

Python is a free program that runs the anti-AFK program.
(Already have Python? Skip to Step 2.)

1. Click the **Start** button, type `Microsoft Store` and open it.
2. In the search box, type **Python Install Manager**.
3. Pick the one made by **Python Software Foundation**.
4. Click **Get** (or **Install**) and wait for it to finish.

### Step 2: Put the files in a folder

1. Make a new folder on your Desktop called `RobloxAntiAFK`.
2. Put the file `anti_afk.py` inside it.

If you got a `.zip` file, right-click it and choose **Extract All** first.

### Step 3: Open the black command window in that folder

1. Open the `RobloxAntiAFK` folder.
2. Click the **address bar** at the top of the window (the bar that shows the folder's name).
3. Type `cmd` and press **Enter**.

A black window opens. This is called the **terminal**. You type commands into it and
press **Enter** to run them.

**Tip:** you can copy a command from this guide and paste it into the black window
with **Ctrl + V**.

### Step 4: Finish setting up Python

In the black window, type this and press **Enter**:

```
python --version
```

The first time, Python finishes setting itself up. If it asks you questions that end in
`[Y/n]` or `[y/N]`, just press **Enter** to go with the suggested answer.

When it's done, you should see something like `Python 3.15.0`. Any number starting with 3 is fine.

### Step 5: Install the helpers

Type this and press **Enter**:

```
python -m pip install pydirectinput pygetwindow
```

Wait until it says **Successfully installed**. Yellow warning messages are OK.

Setup is done! You never need to do Part 1 again.

---

## Part 2: Start it (every time you play)

1. Open Roblox and **join a game**.
2. Open the `RobloxAntiAFK` folder, click the address bar, type `cmd` and press **Enter**
   (just like Step 3).
3. Type this and press **Enter**:

```
python anti_afk.py
```

You should see:

```
Anti-idle running. Ctrl+C to stop.
```

That's it! **Leave the black window open.** You can use other apps now. Roblox can be
behind other windows or minimised.

Every few minutes, a new line shows up, like this:

```
[14:32:10] nudged camera zoom
```

### How to stop it

Click on the black window and press **Ctrl + C**. Or just close the black window.

---

## Good to know

- **Roblox will pop up for about a second every 4 to 8 minutes.** This is normal.
  It waits until you stop typing or moving the mouse for 2 seconds, so it won't
  mess up what you're typing.
- If you're watching a full-screen video or playing another full-screen game,
  it will interrupt it for a second.
- **Don't let the computer go to sleep.** If it sleeps, Roblox disconnects.
  Go to **Settings > System > Power** and set the computer to never sleep while it's
  plugged in. Laptops: keep them plugged in. The screen turning off by itself is fine.
- **Don't lock the computer** (Windows key + L). The program can't press keys while
  the lock screen is showing.
- It does **not** reconnect you if you get disconnected (for example, if the internet
  drops or the server shuts down). You'll need to rejoin yourself.
- In most games, I and O zoom the camera. If your game uses I or O for something else
  (like opening a menu), you might see that happen.

---

## Problems?

**"'python' is not recognized..."**
Python isn't installed yet. Do Step 1 again. Then close the black window, open a new one
(Step 3) and try again.

**"No module named 'pydirectinput'"** (or `'pygetwindow'`)
The helpers aren't installed. Do Step 5.

**"can't open file ... anti_afk.py"**
The black window was opened in the wrong folder. Close it and open a new one from inside
the `RobloxAntiAFK` folder (Step 3).

**"Roblox not found, skipped nudge"**
Roblox isn't open. Join a Roblox game. The program keeps trying by itself, so you don't
need to restart it.

**"Windows didn't let Roblox come to the front, skipped nudge"**
Windows blocked the switch that time. The program will try again in a few minutes.
If it keeps happening, click on the Roblox window yourself once.

**It stopped with a "FailSafeException" error**
Your mouse was in the very top-left corner of the screen. That corner is an emergency
stop button. Move the mouse somewhere else and run `python anti_afk.py` again.

---

## For grown-ups: changing the timing

Right-click `anti_afk.py` and choose **Open with > Notepad**. Near the top you'll see:

```
IDLE_MIN = 4 * 60           # seconds between camera nudges
IDLE_MAX = 8 * 60
USER_QUIET = 2              # seconds without keyboard/mouse use before switching to Roblox
```

`4 * 60` means 4 minutes. The program waits a random time between `IDLE_MIN` and
`IDLE_MAX` before each nudge. Keep `IDLE_MAX` at 15 minutes (`15 * 60`) or less,
because Roblox kicks you after 20 minutes. Save the file, then start the program again.
# roblox-anti-afk
