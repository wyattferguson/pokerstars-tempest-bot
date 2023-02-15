
import re
import cv2
import mss
from typing import Tuple
import numpy as np
import pytesseract as ocr

from config import *

ocr.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Vision():
    def __init__(self) -> None:
        self.snap = mss.mss()

    def cards(self):
        hand = []
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=A2345678910JQK"

        for idx, c in enumerate(CARD_VALUE_LOCAIONS):
            gray_screen = self.screen_shot(c, True)

            card_str = ocr.image_to_string(gray_screen, lang='eng', config=ocr_config)
            card_value = card_str.strip()
            if card_value:
                card_suit = self.card_suit(idx)
                if card_suit:
                    if card_value == 0 or card_value == "10":
                        card_value = "T"
                    elif len(card_value) > 1:  # fix reading 8/9 as 18/19
                        card_value = card_value[1:]

                    hand.append(f"{card_value}{card_suit}")
                else:
                    return []

        return hand

    def card_suit(self, card_idx: int) -> str:
        screen_shot = self.screen_shot(CARD_SUIT_LOCAIONS[card_idx], True)
        suit = False
        threshold = 0.8
        max_suit_score = 0
        for s in SUITS:
            suit_needle = self.load_grey_image(f"{DIR_PATH}\\needles\\{s}.png")
            match_score = self.match_image(screen_shot, suit_needle)

            if match_score > threshold and match_score > max_suit_score:
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
        threshold = 0.85
        timer_needle = self.load_grey_image(f"{DIR_PATH}\\needles\\timer.png")
        screen_shot = self.screen_shot(TIMER_LOCATION, True)
        match_score = self.match_image(screen_shot, timer_needle)
        return match_score > threshold

    def save_image(self, img) -> None:
        img_name = f"{random.randint(1,99999)}"
        isWritten = cv2.imwrite(f"{DIR_PATH}\\snaps\\{img_name}.png", img)

        if isWritten:
            print('Image is successfully saved as file.')

    def read_pot(self) -> int:
        pot_screen = self.screen_shot(POT_LOCATION)
        pot_str = ocr.image_to_string(pot_screen)
        current_pot = re.sub('[^0-9]', '', pot_str.strip())
        return current_pot

    def read_wallet(self) -> int:
        wallet = 0
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789(),"
        screen_shot = self.screen_shot(WALLET_LOCATION)
        wallet_text = ocr.image_to_string(screen_shot, lang='eng', config=ocr_config)
        parsed_wallet = wallet_text[wallet_text.find('(') + 1: wallet_text.find(')')]
        if parsed_wallet:
            wallet = re.sub('[^0-9]', '', parsed_wallet.strip())
        return wallet

    def read_players(self) -> Tuple[bool, int]:
        player_cnt = 0
        player_push = False
        ocr_config = "--psm 13 --oem 1"
        for i, p in enumerate(PLAYER_SEATS):
            status_img = self.screen_shot(p)
            status_str = ocr.image_to_string(status_img, lang='eng', config=ocr_config)
            status = ''.join(filter(str.isalpha, status_str)).lower()

            if status in ['cap', 'allin', 'aln', 'alin', 'anin']:
                player_cnt += 1
                player_push = True
                status = "Called"
            elif status == 'seat':
                status = "Empty Seat"
            else:
                player_cnt += 1
                status = "Waiting"

        #     print(f"Player {i + 1}: {status}")

        # print(f"Total Players: {player_cnt}")
        # print(f"Hands Players: {self.hand_players}")
        # print("\n############################\n")
        return (player_push, player_cnt)

    def screen_shot(self, location: dict, gray_convert: bool = False):
        screen = np.array(self.snap.grab(location))
        if gray_convert:
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            return gray_screen
        return screen

    def popup_image(self, image):
        cv2.imshow('Screen Shot', image)
        cv2.waitKey(1)
        time.sleep(2)


if __name__ == "__main__":
    vsn = Vision()
    while True:
        vsn.read_timer()
