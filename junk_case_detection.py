
import os
import cv2 as cv
import numpy as np
from found_in_raid_detection import *
import pyautogui
import time


def get_junkcase_pos_from_screen_shot(screen_shot, pattern_image, show_off=NO_SHOWOFF):

    list_of_pos = []
    print(screen_shot)
    scanned_image = cv.imread(screen_shot, cv.IMREAD_UNCHANGED)
    pattern = cv.imread(
        pattern_image, cv.IMREAD_UNCHANGED)  # searching target
    result = cv.matchTemplate(
        scanned_image, pattern, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    threshold = 0.90
    locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))
    list_of_pos = list_of_pos + locations

    fir_nbr = len(list_of_pos)
    print(f"This junk box contains {fir_nbr} FIR items")
    if (show_off == SHOWOFF):
        if list_of_pos:
            print('match found')
            fir_w = pattern.shape[1]
            fir_h = pattern.shape[0]
            line_color = (
                0, 0, 255)

            line_type = cv.LINE_4
            for loc in list_of_pos:

                top_left = loc

                bottom_right = (top_left[0] + fir_w, top_left[1] + fir_h)

                cv.rectangle(scanned_image, top_left, bottom_right,
                             color=line_color, thickness=2, lineType=line_type)

            cv.imshow('found', scanned_image)
            cv.waitKey()
        else:
            print("not fir items")
    return list_of_pos


myScreenshot = pyautogui.screenshot()
myScreenshot.save('images//current_screen.png')
image = cv.imread('images//current_screen.png')
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imwrite('images//current_screen.png', gray_image)

sell_tab = "images//junkcase//sell_test.png"
list_sell = get_junkcase_pos_from_screen_shot(
    'images//current_screen.png', sell_tab, show_off=SHOWOFF)
print(list_sell)
