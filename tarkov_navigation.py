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


SHOWOFF = 1
NO_SHOWOFF = 0

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


def look_for_pattern_in_image(search_pattern, searched_image, show_off=NO_SHOWOFF, confidence=.90):
    print(search_pattern)
    scanned_image = cv.imread(searched_image, cv.IMREAD_UNCHANGED)
    pattern = cv.imread(
        search_pattern, cv.IMREAD_UNCHANGED)  # searching target
    result = cv.matchTemplate(
        scanned_image, pattern, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    confidence = 0.90
    locations = np.where(result >= confidence)
    locations = list(zip(*locations[::-1]))

    if (show_off == SHOWOFF):
        if locations:
            print('match found')
            fir_w = pattern.shape[1]
            fir_h = pattern.shape[0]
            line_color = (
                0, 0, 255)

            line_type = cv.LINE_4
            for loc in locations:

                top_left = loc

                bottom_right = (top_left[0] + fir_w, top_left[1] + fir_h)

                cv.rectangle(scanned_image, top_left, bottom_right,
                             color=line_color, thickness=2, lineType=line_type)

            cv.imshow('found', scanned_image)
            cv.waitKey()
        else:
            print("no patterns found in image")
    return locations


def take_screenshot(filepath='images//current_screen.png'):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(filepath)
    image = cv.imread(filepath)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite(filepath, gray_image)
    return filepath


def find_current_tab():
    take_screenshot()
    for tab in tabs:  # tries all the different avaible menus
        print(tab.get_img_file_path())
        if (look_for_pattern_in_image(tab.get_img_file_path(), 'images//current_screen.png')):
            return tab
    return -1


def get_tab_from_value():
    tab = find_current_tab()
    print(tab)
