
import win32gui
import win32process
import psutil
import ctypes
import win32con
import win32api
import time
import os

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(
    ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


def getProcessIDByName(name: str):
    qobuz_pids = []
    process_name = name

    for proc in psutil.process_iter():
        if process_name in proc.name():
            qobuz_pids.append(proc.pid)

    return qobuz_pids


def get_hwnds_for_pid(pid: int):
    def callback(hwnd, hwnds):
        # if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def getWindowTitleByHandle(hwnd: int):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value


def getWindowHandle(name: str):
    pids = getProcessIDByName(name)

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd


def moveWindow(name: str, screenId: int):
    window_handle = getWindowHandle(name)

    screen_width, screen_height = win32api.GetSystemMetrics(
        win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    screen_x, screen_y = screenId * screen_width, 0

    # win32gui.SetForegroundWindow(window_handle)
    time.sleep(0.3)
    win32gui.SetWindowPos(window_handle, win32con.HWND_TOP, screen_x,
                          screen_y, screen_width, screen_height, win32con.SWP_SHOWWINDOW)
    time.sleep(0.3)
    win32gui.ShowWindow(window_handle, 3)


if __name__ == '__main__':
    os.system("start Spotify")
    time.sleep(1)
    moveWindow("Spotify.exe", -1)
    os.system("start Chrome")
    time.sleep(1)
    moveWindow("chrome.exe", 0)
    os.system(
        "start C:\\Users\\timoo\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe")
    time.sleep(6)
    moveWindow("Discord.exe", 1)
