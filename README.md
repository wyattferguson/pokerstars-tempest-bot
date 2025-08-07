# :black_joker: Poker Stars - Tempest Bot

![Tempest Bot Running](screenshot.png)

This is a bot that plays Tempest (aka Push/Fold) poker using OCR and image matching. Push/Fold poker is pretty simple, you are dealt 2 cards and you only have 2 options push(all in) or fold.

The app then uses precalculated Nash push/fold tables to recommend a action(push/fold). Also I precalculated the hand win % in a separate table to also pull in and give you a bit more info about your hand.

Heres some useful reading for more details:

- [PokerStars Tempest](https://www.pokerstars.com/poker/games/tempest/)
- [Nash Push/Fold Tables](https://matchpoker.com/learn/strategy-guides/push-fold-charts)

> [!note]
> This is just a rough proof of concept that you can read cards and interact with the PokerStars app and should be taken with a grain of salt.

## Dev Environment

Installation is using [UV](https://docs.astral.sh/uv/) to manage everything.

**Step 1**: Create a virtual environment

```bash
uv venv
```

**Step 2**: Activate your new environment

```bash
# on windows
.venv\Scripts\activate
```

**Step 3**: Install all the cool dependencies

```bash
uv sync
```

**Step 4**: Next you will need to install Tesseract-OCR:

[Tesseract Download/Install Guide](https://github.com/UB-Mannheim/tesseract/wiki)

Lastly after tesseract is installed you will need to update the _ocr.pytesseract.tesseract_cmd_ in _vision.py_ file with the installation path of tesseract.

## Configuration + Running

All configurations can be found in the _config.py_ file. The big setup challenge will be getting the positions setup for the player. I was using a 2k screen and the game board was snapped to he left using the Windows tile manager and thats how I calculated where everything is. Also your small blind and max push value can be set here also.

In the _vision.py_ file I have a _popup_image_ function that will show any screenshot you pass it so you can use that norrow in your X/Y positions of everything.

Run the app with UV:

```bash
uv run .\src\main.py
```

## License + Legal

This project is provided as is, and is intended for educational purposes only and should not be used to actual gambling.

[MIT License](https://github.com/wyattferguson/pokerstars-tempest-bot/blob/main/LICENSE)

## Contact + Support

Created by [Wyatt Ferguson](https://github.com/wyattferguson)

For any questions or comments heres how you can reach me:

### :octocat: Follow me on [Github @wyattferguson](https://github.com/wyattferguson)

### :mailbox_with_mail: Email me at [wyattxdev@duck.com](wyattxdev@duck.com)

### :tropical_drink: Follow on [BlueSky @wyattf](https://wyattf.bsky.social)
