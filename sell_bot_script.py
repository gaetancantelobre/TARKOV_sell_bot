from pyautogui import *
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api
import win32con
import cv2
import pytesseract
import easyocr
import re
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\TWIM\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


autoselect_same = (639, 55)
autoselect_red = 228
add_offer = (1750, 109)
first_slot = (41, 287)
refresh = (2450, 156)
price_select = (1878, 167)
lowest_price = (1880, 233)
set_price = (1237, 492)
post_offer = (1231, 995)

# status variables

junk_posx = 0
junk_posy = 0

box_dim = 14

grand_total = 0


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def rightClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def doubleClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def lookForOnScreen(filename):
    if (pyautogui.locateOnScreen(filename, grayscale=True, confidence=0.3)):
        return True


def checkColor(pos, red_color):
    if (pyautogui.pixel(pos[0], pos[1])[0] == red_color):
        return True


def checkAutoSelect():
    if (pyautogui.pixel(639, 55)[0] == 27):
        click(639, 55)


def checkLowestPrice():
    if (pyautogui.pixel(1910, 162)[0] != 195):
        click(1910, 162)


def checkOfferSlot():
    click(2449, 160)
    win32api.SetCursorPos((add_offer[0], add_offer[1]))
    time.sleep(1)
    if (pyautogui.pixel(add_offer[0], add_offer[1])[0] > 50):
        return True
    else:
        return False


def moveWindow(clickpos, targetpos):
    win32api.SetCursorPos(clickpos)
    pyautogui.dragTo(targetpos[0], targetpos[1], duration=0.2)
    click(0, 1439)


def sellSetup():
    click(1658, 1415)  # open flea market
    if checkOfferSlot():
        click(add_offer[0], add_offer[1])
    else:
        exit("no offer available")
    moveWindow((997, 404), (0, 0))  # move inventory window to top right
    rightClick(40, 126)
    time.sleep(0.5)
    click(126, 171)  # open junkbox
    time.sleep(0.6)
    moveWindow((1333, 125), (0, 1435))  # move junkbox inventory to bottomright
    checkAutoSelect()


def getRoubleValueFromScreenShot():
    originalImage = cv2.imread('images//price.png')
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    (_, blackAndWhiteImage) = cv2.threshold(
        grayImage, 127, 255, cv2.THRESH_BINARY_INV)
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(blackAndWhiteImage)
    cv2.imwrite("images//bnwprice.png", blackAndWhiteImage)

    final_price = ""
    for i in results:
        str = i[1]
        str = str.replace('s', '5').replace(
            'S', '5').replace('@', '0').replace('g', '9')
        if len(i[1]) > 3:
            str = str[:-1]
        final_price += str

    final_price = re.sub(r'[^0-9]', '', final_price)
    print("Lowest market price : " + final_price)
    return int(final_price)


def takeScreenShotOfPrice():
    click(2442, 162)
    im2 = pyautogui.screenshot(
        'images//price.png', region=(1779, 210, 210, 45))


def sellSetup():
    time.sleep(3)
    click(1661, 1419)  # open flea market from inventory
    time.sleep(1)
    click(1640, 107)  # add offer
    time.sleep(1)
    rightClick(40, 126)  # open junk menu
    time.sleep(0.5)
    click(126, 171)  # open junkbox
    time.sleep(0.6)
    moveWindow((1333, 125), (0, 1435))  # move junkbox inventory to bottomright
    checkAutoSelect()  # check or uncheck auto select tab
    checkLowestPrice()


def setPriceAndSell(value, margin):
    click(1409, 492)  # clear price just in case
    time.sleep(0.5)
    click(1297, 492)  # select rubles
    time.sleep(1)
    if (value > 30000):
        margin = 1000
    else:
        margin = 500
    pyautogui.typewrite(str(value-margin), 0.2)
    print(f"Item put on market for {value} - {margin} :" + str(value - margin))
    addSellToFile(recap, (value - margin))
    time.sleep(0.5)
    click(1290, 991)


def sellItems():
    click(1640, 107)  # add offer
    time.sleep(1)
    rightClick(40, 126)  # open junk menu
    time.sleep(0.5)
    click(126, 171)  # open junkbox
    time.sleep(0.6)
    moveWindow((1333, 125), (0, 1435))  # move junkbox inventory to bottomright
    checkAutoSelect()  # check or uncheck auto select tab
    checkLowestPrice()
    posx = 65+(junk_posx*85)
    posy = 300+(junk_posy*85)
    # check for empty slot to avoid errors
    if (pyautogui.pixel(posx, posy)[0] != pyautogui.pixel(posx, posy)[1]):
        click(posx, posy)  # highlight wanted item
        time.sleep(0.3)
        rightClick(posx, posy)  # open item menu
        time.sleep(1)
        click((posx + 30), (posy+80))  # filter by item
        time.sleep(1)
        takeScreenShotOfPrice()
        price = getRoubleValueFromScreenShot()
        setPriceAndSell(price, 500)
    else:
        click(1184, 236)  # closing junkcase window
        time.sleep(0.2)
        click(1450, 11)  # closing junkcase window


# sellSetup()
while (keyboard.is_pressed('q') == False):
    if (junk_posy < box_dim):
        if (checkOfferSlot()):
            sellItems()
            if (junk_posx == box_dim):
                junk_posx = 0
                junk_posy += 1
            else:
                junk_posx += 1
        time.sleep(1)
    else:
        break
print("done")
