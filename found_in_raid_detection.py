import os
import cv2 as cv
import numpy as np

SHOWOFF = 1
NO_SHOWOFF = 0


def get_list_of_fir_templates():
    fir_template = os.listdir('fir_templates')
    modified_firs = []
    for fir in fir_template:
        modified_firs.append('fir_templates//' + fir)
    return modified_firs


def distance(point1, point2):  # calculates the distance between points
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# goes through each point if its unique or not close to other point it will and add it to the new list
# goes through each point and makes sure that it is on the left side of the screen
def clean_points(point_list, threshold=3):
    cleaned_list = []
    for point in point_list:
        is_duplicate = False
        for existing_point in cleaned_list:
            if distance(point, existing_point) < threshold or point[0] > 2560/2:
                is_duplicate = True
                break
        if not is_duplicate:
            cleaned_list.append(point)
    return cleaned_list


def get_fir_pos_from_screen_shot(screen_shot, show_off=NO_SHOWOFF):
    list_of_pos = []
    fir_types = get_list_of_fir_templates()

    for fir_type in fir_types:

        scanned_image = cv.imread(screen_shot, cv.IMREAD_UNCHANGED)
        fir_image = cv.imread(fir_type, cv.IMREAD_UNCHANGED)

        result = cv.matchTemplate(
            scanned_image, fir_image, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        threshold = 0.75
        locations = np.where(result >= threshold)

        locations = list(zip(*locations[::-1]))
        list_of_pos = list_of_pos + locations

    list_of_pos = clean_points(list_of_pos, 3)

    fir_nbr = len(list_of_pos)
    print(f"This junk box contains {fir_nbr} FIR items")
    if (show_off == SHOWOFF):
        if list_of_pos:
            print('match found')
            fir_w = fir_image.shape[1]
            fir_h = fir_image.shape[0]
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


# get_fir_pos_from_screen_shot('flea_market_example.png', SHOWOFF)
