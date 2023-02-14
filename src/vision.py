
import re

import cv2
import keyboard
import mss
import numpy
import pytesseract as ocr
from PIL import Image, ImageOps

from config import *

ocr.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

IMG_PATH = 'C:\\Code\\poker\\src'


class Vision():
    def __init__(self, delay: int = 1) -> None:
        self.delay = delay
        self.snap = mss.mss()

    def blind(self):
        pass

    def cards(self):
        hand = []
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=A2345678910JQK"
        # image_file = 'C:\\Code\\poker\\src\\two.png'
        # img = Image.open(image_file)
        # grey_scale = ImageOps.grayscale(img)

        # self.popup_image(numpy.array(grey_scale))

        # for idx, c in enumerate(CARD_VALUE_LOCAIONS):
        #     screen_shot = self.screen_shot(c)
        #     gray_screen = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2GRAY)

        #     screen_str = ocr.image_to_string(gray_screen, lang='eng', config=ocr_config)
        #     card_value = screen_str.strip()
        #     if card_value:
        #         card_suit = self.card_suit(idx)
        #         if card_value == 0:
        #             card_value = "T"
        #         hand.append(f"{card_value}{card_suit}")
        #         print(f"CARD: {card_value}")
        #     else:
        #         print(f"NO CARD FOUND")
        #     # self.popup_image(gray_screen)

        for s in CARD_SUIT_LOCAIONS:
            screen_shot = self.screen_shot(s)
            self.popup_image(screen_shot)

        return hand

    def save_image(self, img):
        # save matrix/array as image file
        img_name = f"{random.randint(1,99999)}"
        isWritten = cv2.imwrite(f"{IMG_PATH}\\suits\\{img_name}.png", img)

        if isWritten:
            print('Image is successfully saved as file.')

    def card_suit(self, card_idx: int) -> str:
        screen_shot = self.screen_shot(CARD_SUIT_LOCAIONS[card_idx])

        card_suit_part = "c"
        card_img = cv2.imread(
            f"{IMG_PATH}\\suits\\{card_suit_part}{card_idx}.png")
        card_sect = numpy.array(card_img)
        scr_remove = card_sect[:, :, :3]

        result = cv2.matchTemplate(
            scr_remove, screen_shot, cv2.TM_CCOEFF_NORMED)
        print(result)

    def pot(self) -> int:
        pot_screen = self.screen_shot(POT_LOCATION)
        pot_str = ocr.image_to_string(pot_screen)
        current_pot = re.sub('[^0-9]', '', pot_str.strip())
        print(f"Pot: {current_pot}")
        return current_pot

    def game_state(self):
        pass

    def screen_shot(self, location):
        return numpy.array(self.snap.grab(location))

    def popup_image(self, image):
        cv2.imshow('Screen Shot', image)
        cv2.waitKey(1)
        time.sleep(5)


if __name__ == "__main__":
    delay = 1
    vsn = Vision(delay)
    # print("Press 's' to start playing.")
    # keyboard.wait('s')

    while True:
        # vsn.pot()
        hand = vsn.cards()
        print("Hand: ", hand)
        time.sleep(delay)
