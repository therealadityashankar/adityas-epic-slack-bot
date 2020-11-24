#!/usr/bin/env python3
# production url : https://playground-email-1600840828782.uc.r.appspot.com/slack/events
import os
import yaml
import requests

# Use the package we installed
from slack_bolt import App
from config import config
from adibot_show import adibot_show_service
from adibot_make import adibot_make_service
from adibot_meme import adibot_meme_service


# Initializes your app with your bot token and signing secret
app = App(token=config["token"], signing_secret=config["signing_secret"])


@app.message("adi-bot")
def adibotservice(message, say):
    text = message["text"].strip()
    words = [word.strip() for word in text.split(" ") if word.strip() != ""]

    if not words[0] == "adi-bot":
        return

    if len(words) == 1:
        say(
            "you can see all of adi-bot's features at its docs at \
https://github.com/therealadityashankar/adityas-epic-slack-bot"
        )
        return

    elif words[1] == "show":
        return adibot_show_service(message, say, words)

    elif words[1] == "make":
        return adibot_make_service(message, say, words)

    elif words[1] == "meme":
        return adibot_meme_service(message, say, words)

    else:
        say(f"I could not understand the command `{text}`")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
