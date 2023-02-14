""""
- Card suit, determine color scores to use
- Add red check for your turn on the red buttons in the bottom right
- setup poker key short cuts

"""
import re
import cv2
import keyboard
import mss
import numpy as np
import pytesseract as ocr

from config import *

ocr.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Vision():
    def __init__(self, delay: int = 1) -> None:
        self.delay = delay
        self.players = 0
        self.pot = 0
        self.hand_players = 0
        self.hand = []
        self.games = 1
        self.call = False
        self.wallet = 1000
        self.snap = mss.mss()

    def blind(self):
        pass

    def cards(self):
        hand = []
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=A2345678910JQK"

        for idx, c in enumerate(CARD_VALUE_LOCAIONS):
            gray_screen = self.screen_shot(c, True)

            card_str = ocr.image_to_string(gray_screen, lang='eng', config=ocr_config)
            card_value = card_str.strip()
            if card_value:
                # card_suit = self.card_suit(idx)
                if card_value == 0:
                    card_value = "T"
                hand.append(f"{card_value}")
                # print(f"CARD: {card_value}")
            else:
                print(f"NO CARD FOUND")
            # self.popup_image(gray_screen)

        print(hand)

        return hand

    def card_suit(self, card_idx: int) -> str:
        '''
        NO HAND / EMPTY SEAT: [ 56.  52.  50. 255.]
        CARD IN HAND:
        SPADE:
        HEARTS:
        DIAMONDS:
        CLUBS:
        '''

        screen_shot = self.screen_shot(CARD_SUIT_LOCAIONS[card_idx])
        avg_color_per_row = np.average(screen_shot, axis=0)
        img_avg = np.round_(np.average(avg_color_per_row, axis=0), decimals=0)
        # @ red_value = img_avg.flat[0]
        print(img_avg)
        self.popup_image(screen_shot)

    def clear_board(self):
        self.hand = []
        self.pot = 0
        self.action = False
        self.hand_players = 0
        self.games += 1

    def save_image(self, img):
        # save matrix/array as image file
        img_name = f"{random.randint(1,99999)}"
        isWritten = cv2.imwrite(f"{DIR_PATH}\\suits\\{img_name}.png", img)

        if isWritten:
            print('Image is successfully saved as file.')

    def read_pot(self) -> int:
        pot_screen = self.screen_shot(POT_LOCATION)
        pot_str = ocr.image_to_string(pot_screen)
        current_pot = re.sub('[^0-9]', '', pot_str.strip())
        if self.pot != current_pot:
            self.pot = current_pot
            print(f"Pot: {self.pot}")
        return current_pot

    def read_wallet(self) -> int:
        ocr_config = "--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789(),"
        screen_shot = self.screen_shot(WALLET_LOCATION)
        wallet_text = ocr.image_to_string(screen_shot, lang='eng', config=ocr_config)
        parsed_wallet = wallet_text[wallet_text.find('(') + 1: wallet_text.find(')')]
        if parsed_wallet:
            self.wallet = re.sub('[^0-9]', '', parsed_wallet.strip())
            print("Wallet: ", self.wallet)
        return self.wallet

    def read_players(self):
        player_cnt = 0
        self.hand_players = 0
        ocr_config = "--psm 13 --oem 1"
        for i, p in enumerate(PLAYER_SEATS):
            status_img = self.screen_shot(p)
            # self.popup_image(status_img)
            status_str = ocr.image_to_string(status_img, lang='eng', config=ocr_config)
            status = ''.join(filter(str.isalpha, status_str)).lower()
            # print(status)
            if status in ['cap', 'allin', 'aln', 'alin', 'anin']:
                player_cnt += 1
                self.call = True
                status = "Called"
                self.hand_players += 1
            elif status == 'seat':
                status = "Empty Seat"
            else:
                player_cnt += 1
                status = "Waiting"

            print(f"Player {i + 1}: {status}")

        print(f"Total Players: {player_cnt}")
        print(f"Hands Players: {self.hand_players}")
        print("\n############################\n")
        self.players = player_cnt

    def game_state(self):
        pass

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

    def __str__(self) -> str:
        return f"POT: {self.pot} | PLYS: {self.players} | WLT: {self.wallet} | GMS: {self.games} | HND: {self.hand}"


if __name__ == "__main__":
    delay = 1
    vsn = Vision(delay)
    # print("Press 's' to start playing.")
    # keyboard.wait('s')

    while True:
        # vsn.read_pot()
        # vsn.read_players()
        # hand = vsn.cards()
        vsn.card_suit(0)
        # print("Hand: ", hand)
        # vsn.read_wallet()
        time.sleep(delay)
