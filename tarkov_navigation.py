import os
import cv2 as cv
import numpy as np
import pyautogui
import keyboard
import time
import win32api
import win32con

from menu_tabs import *

from PIL import Image

MAIN_MENU = 0
INVENTORY = 1
TRADERS = 2
FLEA_MARKET = 3


def click(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def go_to_tab(tab: Menu_tab) -> None:
    click(tab.get_pos())
    time.sleep(1)


def look_for_pattern_in_image(search_pattern, searched_image):
    print(search_pattern)
    scanned_image = cv.imread(searched_image, cv.IMREAD_UNCHANGED)
    tab_image = cv.imread(
        search_pattern, cv.IMREAD_UNCHANGED)  # searching target
    result = cv.matchTemplate(
        scanned_image, tab_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    threshold = 0.90
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    if (len(locations) < 1):
        return False
    else:
        return True


def find_current_tab():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('images//current_screen.png')
    image = cv.imread('images//current_screen.png')
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite('images//current_screen.png', gray_image)
    time.sleep(1)

    for tab in tabs:  # tries all the different avaible menus
        if (look_for_pattern_in_image(tab.get_img_file_path(), 'images//current_screen.png')):
            return tab
    return -1


def get_tab_from_value():
    tab = find_current_tab()
    print(tab)


get_tab_from_value()
