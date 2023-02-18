
import re
import cv2
import mss
import numpy as np
import pytesseract as ocr
from card import Card
from config import *

ocr.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Vision():
    def __init__(self) -> None:
        self.snap = mss.mss()
        self.threshold = 0.65

    def cards(self) -> list[Card, Card]:
        hand = []

        for idx, c in enumerate(CARD_VALUE_LOCAIONS):
            grey_card = self.screen_shot(c, True)
            card_value = False
            best_score = 0

            # self.popup_image(grey_card)
            for n in ALL_CARDS:
                card_needle = self.load_grey_image(f"{DIR_PATH}\\needles\\{n}.png")
                match_score = self.match_image(grey_card, card_needle)

                if match_score > self.threshold and match_score > best_score:
                    # print(match_score, n)
                    best_score = match_score
                    card_value = n
            if card_value and best_score > self.threshold:
                card_suit = self.card_suit(idx)

                # print(card_value, card_suit)
                if card_suit:
                    hand.append(Card(card_value, card_suit))
                else:
                    return []

        return hand

    def card_suit(self, card_idx: int) -> str:
        grey_suit = self.screen_shot(CARD_SUIT_LOCAIONS[card_idx], True)
        suit = False
        max_suit_score = 0

        # self.popup_image(grey_suit)
        for s in SUITS:
            suit_needle = self.load_grey_image(f"{DIR_PATH}\\needles\\{s}.png")
            match_score = self.match_image(grey_suit, suit_needle)

            if match_score > self.threshold and match_score > max_suit_score:
                max_suit_score = match_score
                suit = s

        return suit

    def match_image(self, image, needle) -> float:
        scores = cv2.matchTemplate(image, needle, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(scores)
        return round(max_val, 3)

    def load_grey_image(self, img_path: str):
        img = cv2.imread(img_path)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_grey

    def read_timer(self) -> bool:
        threshold = 0.75
        timer_needle = self.load_grey_image(f"{DIR_PATH}\\needles\\timer.png")
        screen_shot = self.screen_shot(TIMER_LOCATION, True)
        # self.popup_image(screen_shot)
        match_score = self.match_image(screen_shot, timer_needle)
        # print(match_score)
        return match_score > threshold

    def save_image(self, img) -> None:
        name_tag = f"{random.randint(1,99999)}"
        img_name = f"{DIR_PATH}\\snaps\\{name_tag}.png"
        is_written = cv2.imwrite(img_name, img)

        if is_written:
            print(f'Saved: {img_name}')

    def read_pot(self) -> float:
        screen_img = self.screen_shot(POT_LOCATION)
        # self.popup_image(screen_img)
        img_str = ocr.image_to_string(screen_img)
        values = re.sub('[^0-9^.]', '', img_str.strip())
        return float(values) if values else False

    def read_wallet(self):
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789.$"
        screen_img = self.screen_shot(WALLET_LOCATION)
        img_str = ocr.image_to_string(screen_img, lang='eng', config=ocr_config)
        values = re.sub('[^0-9^.]', '', img_str.strip())
        return values

    def screen_shot(self, location: dict, gray_convert: bool = False) -> np.array:
        screen = np.array(self.snap.grab(location))
        if gray_convert:
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            return gray_screen
        return screen

    def popup_image(self, image) -> None:
        cv2.imshow('Screen Shot', image)
        cv2.waitKey(1)
        time.sleep(1)


if __name__ == "__main__":
    pass
    vsn = Vision()
    while True:
        #     # pot = vsn.read_pot()
        #     # print(pot)
        #     wallet = vsn.read_wallet()
        #     print(wallet)
        cards = vsn.cards()
        print(cards)
        # print(vsn.read_timer())
        time.sleep(1)
