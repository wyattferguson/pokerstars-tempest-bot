
import re
import cv2
import mss
import numpy as np
import pytesseract as ocr
from card import Card
from config import *

ocr.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Vision():
    """ Read information from PokerStars table """

    def __init__(self) -> None:
        self.snap = mss.mss()
        self.threshold = 0.65

    def cards(self) -> list[Card, Card]:
        """ Try to read players hand from table """
        hand = []

        for idx, c in enumerate(CARD_VALUE_LOCAIONS):
            grey_card = self.screen_shot(c, True)

            card_value = False
            best_score = 0

            # compare all card needles against player card screenshot
            for n in ALL_CARDS:
                card_needle = self.load_grey_image(f"{CARD_PATH}{n}.png")
                match_score = self.match_image(grey_card, card_needle)

                if match_score > self.threshold and match_score > best_score:
                    best_score = match_score
                    card_value = n

            if card_value and best_score > self.threshold:
                card_suit = self.card_suit(idx)

                if card_suit:
                    hand.append(Card(card_value, card_suit))
                else:
                    return []  # return nothing if it cant find both cards value/suit

        return hand

    def card_suit(self, card_idx: int) -> str:
        """ Try to determine a suit for a given player card """
        grey_suit = self.screen_shot(CARD_SUIT_LOCAIONS[card_idx], True)

        suit = False
        max_suit_score = 0

        for s in SUITS:
            suit_needle = self.load_grey_image(f"{CARD_PATH}{s}.png")
            match_score = self.match_image(grey_suit, suit_needle)
            if match_score > self.threshold and match_score > max_suit_score:
                max_suit_score = match_score
                suit = s

        return suit

    def match_image(self, image: list, needle: list) -> float:
        """ Compare given image to needle """
        scores = cv2.matchTemplate(image, needle, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(scores)
        return round(max_val, 2)

    def load_grey_image(self, img_path: str) -> list:
        """ Load a given image and convert it to grey scale """
        img = cv2.imread(img_path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def read_timer(self) -> bool:
        """ Has the player timer appeared below his profile """
        timer_needle = self.load_grey_image(f"{CARD_PATH}timer.png")
        screen_shot = self.screen_shot(TIMER_LOCATION, True)
        match_score = self.match_image(screen_shot, timer_needle)
        return match_score > self.threshold

    def read_pot(self) -> float:
        """ Current value of table pot """
        screen_img = self.screen_shot(POT_LOCATION)
        img_str = ocr.image_to_string(screen_img)
        values = re.sub('[^0-9^.]', '', img_str.strip())
        return float(values) if values else False

    def read_wallet(self) -> float:
        """ Get the players current wallet """
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789,()"
        screen_img = self.screen_shot(WALLET_LOCATION)
        img_str = ocr.image_to_string(screen_img, lang='eng', config=ocr_config)
        parsed_img = img_str[0: img_str.find('(')]
        return re.sub('[^0-9^.]', '', parsed_img.strip())

    def screen_shot(self, location: dict, gray_convert: bool = False) -> np.array:
        """ Take a screen shot of the table at a given location """
        screen = np.array(self.snap.grab(location))
        if gray_convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        return screen

    def popup_image(self, image: list) -> None:
        """ Show given image in a popup windows for a short period """
        cv2.imshow('Screen Shot', image)
        cv2.waitKey(1)
        time.sleep(1)


if __name__ == "__main__":
    pass
