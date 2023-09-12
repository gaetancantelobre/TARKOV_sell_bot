from PIL import Image
import os
import cv2

fir_template = os.listdir('menu_tabs')
modified_firs = []
for fir in fir_template:
    modified_firs.append('menu_tabs//' + fir)

for tab in modified_firs:
    image = cv2.imread(tab)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(tab, gray_image)
