#!/usr/bin/env python3
# production url : https://playground-email-1600840828782.uc.r.appspot.com/slack/events
import os
import yaml
import requests

# Use the package we installed
from slack_bolt import App
from config import config
from adibot_show import adibot_show_service

# Initializes your app with your bot token and signing secret
app = App(token=config["token"], signing_secret=config["signing_secret"])


@app.message("adi-bot")
def adibotservice(message, say):
    text = message["text"].strip()
    words = [word.strip() for word in text.split(" ") if word.strip() != ""]

    if not text.startswith("adi-bot"):
        return

    if text == "adi-bot":
        say(
            "you can see all of adi-bot's features at its docs at \
https://github.com/therealadityashankar/adityas-epic-slack-bot"
        )
        return

    elif text.startswith("adi-bot show"):
        return adibot_show_service(message, say, words)

    else:
        say(f"I could not understand the command `{text}`")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
