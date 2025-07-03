import os
import time
import ctypes
import win32gui
import pygetwindow as gw

# 全局状态
_opened_windows = []
_current_position = [0, 0]
_min_size = None

def get_screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect[2] - rect[0], rect[3] - rect[1]

def find_min_window_size(hwnd, min_w=150, min_h=100, step=10):
    width, height = 800, 600
    while width >= min_w and height >= min_h:
        win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
        time.sleep(0.05)
        real_w, real_h = get_window_size(hwnd)
        if real_w != width or real_h != height:
            width += step
            height += step
            break
        width -= step
        height -= step
    return width, height

def move_window(hwnd, x, y, width, height):
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

def record_and_tile_window_if_needed(file_path: str):
    """打开文件并将其窗口记录和平铺（Windows 专用）"""
    global _opened_windows, _current_position, _min_size

    # 打开前窗口列表
    existing_titles = set(gw.getAllTitles())

    os.startfile(file_path)
    time.sleep(1.5)

    # 找到新窗口
    new_windows = [
        w for w in gw.getAllWindows()
        if w.title.strip() and w.title not in existing_titles
    ]
    if not new_windows:
        print(f"[!] 未找到打开文件的窗口: {file_path}")
        return

    hwnd = new_windows[0]._hWnd
    _opened_windows.append(hwnd)

    # 初始化最小尺寸（只探测一次）
    if _min_size is None:
        w, h = find_min_window_size(hwnd)
        _min_size = (w, h)
    else:
        w, h = _min_size

    # 平铺计算
    screen_w, screen_h = get_screen_size()
    x, y = _current_position
    move_window(hwnd, x, y, w, h)

    # 更新下一个窗口位置
    x += w
    if x + w > screen_w:
        x = 0
        y += h
    _current_position = [x, y]
