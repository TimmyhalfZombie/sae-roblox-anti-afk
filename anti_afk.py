import ctypes
import ctypes.wintypes
import random
import time
from contextlib import contextmanager

import pydirectinput
import pygetwindow as gw

# Use real pixel coordinates even with Windows display scaling (125%, 150%...)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

pydirectinput.FAILSAFE = True

# ---------------- settings ----------------
IDLE_MIN = 4 * 60           # seconds between camera nudges
IDLE_MAX = 8 * 60
USER_QUIET = 2              # seconds without keyboard/mouse use before switching to Roblox
# ------------------------------------------


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.wintypes.UINT), ("dwTime", ctypes.wintypes.DWORD)]


def now():
    return time.strftime("%H:%M:%S")


def find_roblox():
    """The Roblox window, preferring one that isn't minimised."""
    wins = [w for w in gw.getAllWindows() if w.title.strip() == "Roblox"]
    wins.sort(key=lambda w: w.isMinimized)
    return wins[0] if wins else None


def focus_window(hwnd):
    """Windows blocks background apps from stealing focus; try several ways around it."""
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    # 1) Borrow the current front window's input "permission"
    fg = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg, None)
    my_thread = kernel32.GetCurrentThreadId()
    attached = bool(fg_thread and fg_thread != my_thread and
                    user32.AttachThreadInput(my_thread, fg_thread, True))
    try:
        if user32.IsIconic(hwnd):           # only un-minimise; never resize a maximised window
            user32.ShowWindow(hwnd, 9)
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
        user32.SetFocus(hwnd)
    finally:
        if attached:
            user32.AttachThreadInput(my_thread, fg_thread, False)
    time.sleep(0.5)
    if user32.GetForegroundWindow() == hwnd:
        return True

    # 2) Alt tap trick
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    return user32.GetForegroundWindow() == hwnd


def bring_to_front(win):
    return focus_window(win._hWnd)


def seconds_since_input():
    info = LASTINPUTINFO(ctypes.sizeof(LASTINPUTINFO), 0)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info))
    return ((ctypes.windll.kernel32.GetTickCount() - info.dwTime) & 0xFFFFFFFF) / 1000


def wait_until_quiet():
    """Wait (up to a minute) for a short break in your typing/mouse use,
    so the quick switch to Roblox doesn't swallow your keystrokes."""
    end = time.time() + 60
    while seconds_since_input() < USER_QUIET and time.time() < end:
        time.sleep(0.2)


def cursor_pos():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


@contextmanager
def borrowed_focus(win):
    """Bring Roblox to the front for a moment, then give focus and the mouse
    back to whatever you were using. Yields whether Roblox made it to the front."""
    user32 = ctypes.windll.user32
    hwnd = win._hWnd
    if user32.GetForegroundWindow() != hwnd:
        wait_until_quiet()
    prev = user32.GetForegroundWindow()
    if prev == hwnd:
        yield True               # already in front, nothing to give back
        return
    was_minimised = user32.IsIconic(hwnd)
    mouse = cursor_pos()
    try:
        yield bring_to_front(win)
    finally:
        if prev:
            focus_window(prev)
        if was_minimised:
            user32.ShowWindow(hwnd, 7)      # minimise again without taking focus
        user32.SetCursorPos(*mouse)


def main():
    print("Anti-idle running. Ctrl+C to stop.")
    while True:
        time.sleep(random.randint(IDLE_MIN, IDLE_MAX))
        win = find_roblox()
        if not win:
            print(f"[{now()}] Roblox not found, skipped nudge")
            continue
        with borrowed_focus(win) as in_front:
            if in_front:
                pydirectinput.press("i")
                time.sleep(0.3)
                pydirectinput.press("o")
                print(f"[{now()}] nudged camera zoom")
            else:
                print(f"[{now()}] Windows didn't let Roblox come to the front, skipped nudge")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped.")
