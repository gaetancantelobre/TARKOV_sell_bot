from tarkov_navigation import look_for_pattern_in_image, take_screenshot, SHOWOFF, NO_SHOWOFF
import pyautogui
from found_in_raid_detection import get_fir_pos_from_screen_shot
import time
import cv2
import easyocr
import win32api
import re

RUB = 0
EUR = 1
USD = 2


class Listing:
    def __init__(self, currency, auto):
        self.currency = currency
        self.auto_select = auto

    currency = RUB
    currency_paths = ['images//currency//roubles.png',
                      'images//currency//usd.png', 'images//currency//euro.png',]
    scroll_position = (0, 0)
    drag_position = (0, 0)
    stash_window_position = (0, 0)
    price = 0
    refresh = (2450, 156)
    add_offer = (1330, 990)

    def toggle_auto_select(self):
        if (self.auto_select):
            auto_pos = look_for_pattern_in_image(
                'images//listing//auto_false.png', take_screenshot(), show_off=NO_SHOWOFF, confidence=0.85)
            if len(auto_pos) > 0:
                print("click")
                pyautogui.click(auto_pos[0][0]+20, auto_pos[0][1]+20)

    def find_scroll_drag_position(self):
        pos = look_for_pattern_in_image(
            'images//listing//stash.png', take_screenshot(), show_off=NO_SHOWOFF)
        if (len(pos) > 0):
            self.stash_window_position = pos[0]
            self.scroll_position = (pos[0][0], pos[0][1]+100)
            self.drag_position = (pos[0][0], pos[0][1]-20)

    def scroll_down_listing(self, nbr_rows):
        win32api.SetCursorPos(self.scroll_position)
        for i in range(4):
            pyautogui.scroll(nbr_rows)

    def find_sell_logo(self):
        junkcase_pos = []
        # while (junkcase_pos == []):
        for i in range(14):
            junkcase_pos = look_for_pattern_in_image(
                'images//junkcase//sell_tag_small.png', take_screenshot(), NO_SHOWOFF, 0.6)
            if (len(junkcase_pos) > 0):
                return junkcase_pos
            self.scroll_down_listing(-4)

    def open_container(self, loc):
        pyautogui.rightClick(loc[0][0]+5, loc[0][1]+5)
        button_pos = look_for_pattern_in_image(
            'images//junkcase//open_tab.png', take_screenshot())
        if (len(button_pos) < 1):
            print("can find menu for opeing container")
            exit()
        else:
            pyautogui.click(button_pos[0][0]+5, button_pos[0][1]+5)

    def find_container_screen(self):
        window = look_for_pattern_in_image(
            'images//junkcase//mag.png', take_screenshot())
        if (len(window) < 1):
            print("can find menu for opeing container")
            exit()
        return window

    def moveWindow(self, clickpos, targetpos):
        win32api.SetCursorPos(clickpos)
        pyautogui.dragTo(targetpos[0], targetpos[1], duration=1)

    def find_price_of_selected_item(self):
        pyautogui.click(self.refresh[0], self.refresh[1])
        time.sleep(1)
        im2 = pyautogui.screenshot(
            'images//price.png', region=(1779, 210, 210, 45))
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
        self.price = int(final_price)

    def filter_by_item(self, fir_pos):
        pyautogui.rightClick(fir_pos[0][0]-5, fir_pos[0][1]-5)
        pos = look_for_pattern_in_image(
            'images//junkcase//filter.png', take_screenshot(), NO_SHOWOFF)
        pyautogui.click(pos[0][0], pos[0][1])

    def select_and_insert_price(self, fir_pos):  # USD // EUR
        pyautogui.click(fir_pos[0][0], fir_pos[0][1])
        pos = look_for_pattern_in_image(
            self.currency_paths[self.currency], take_screenshot(), NO_SHOWOFF)
        if (len(pos) < 1):
            print("couldnt select item in junkcase")
            exit()
        pyautogui.click(pos[0][0]-40, pos[0][1])

        if (self.price > 30000):
            margin = 1000
        else:
            margin = 500
        pyautogui.typewrite(str(self.price-margin), 0.2)
        print(
            f"Item put on market for {self.price} - {margin} :" + str(self.price - margin))
        pyautogui.click(self.add_offer[0], self.add_offer[1])

    def create_listing(self):
        self.toggle_auto_select()
        self.find_scroll_drag_position()
        sell_case_loc = self.find_sell_logo()
        self.open_container(sell_case_loc)
        self.moveWindow(self.find_container_screen()[0], (1, 1))
        fir_pos = get_fir_pos_from_screen_shot(take_screenshot(), NO_SHOWOFF)
        self.filter_by_item(fir_pos)
        self.find_price_of_selected_item()
        self.select_and_insert_price(fir_pos)


print("qdzqzd")
time.sleep(2)
listing = Listing(RUB, True)
listing.create_listing()
