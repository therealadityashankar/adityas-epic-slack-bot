#!/usr/bin/env python3
# production url : https://playground-email-1600840828782.uc.r.appspot.com/slack/events
import os
import yaml
import requests
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
with open("config.yaml") as f:
    config = yaml.safe_load(f)
    app = App(
        token=config['token'],
        signing_secret=config['signing_secret']
    )

@app.message("what is")
def say_hello(message, say):
    user = message['user']
    if user == "WC8S2N2BX" or user == "W0155TCBVUP":
        say(f"look at this person asking stupid questions `{message['text']}`")

@app.message("adi-bot")
def adibotservice(message, say):
    text = message['text'].strip()

    if text == "adi-bot":
        say("you can see all of adi-bot's features at its docs at https://github.com/therealadityashankar/adityas-epic-slack-bot")
        return

    elif text.startswith("adi-bot show"):
        return adibot_show_service(message, say)

def adibot_show_service(message, say):
    begin = "adi-bot show"
    text = message['text'].strip()

    # removes begin string and an additional space after that
    resttext = text[len(begin) + 1:]

    if not text.startswith(begin): return

    if text == begin:
        say("to see a list of options of what adi-bot can show, see https://github.com/therealadityashankar/adityas-epic-slack-bot")

    elif resttext == "cat":
        resp = requests.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key":config['CAT_API_KEY']})
        cat_image_url = resp.json()[0]['url']
        img_block = {"type": "image", "image_url":cat_image_url, "alt_text": "cat image"} 
        text_block = {"type":"section", "text": {"type":"mrkdwn", "text":"here is a cat pic"}}
        blocks = [img_block,  text_block]
        say(blocks=blocks)

    # basically it ends in cats and it has one word in between
    elif resttext.endswith(" cats") and (not " " in resttext[:-len(" cats")]):
        num = resttext[:-len(" cats")]

        try:
            num = int(num)
        except ValueError:
            say(f"{num} could not be converted into an integer")
            return

        if num > 3 or num < 1:
            say(f"the number (what you've said as {num}) should be between 1 and 3")
            return

        resp = requests.get(f"https://api.thecatapi.com/v1/images/search?limit={num}", headers={"x-api-key":config['CAT_API_KEY']})
        blocks = []

        for cat_pic in resp.json():
            cat_image_url = cat_pic['url']
            img_block = {"type": "image", "image_url":cat_image_url, "alt_text": "cat image"} 
            blocks.append(img_block)

        text_block = {"type":"section", "text": {"type":"mrkdwn", "text":f"here are {num} a cat pics"}}
        blocks.append(text_block)

        say(blocks=blocks)

    elif resttext == "dog":
        resp = requests.get("https://api.thedogapi.com/v1/images/search", headers={"x-api-key":config['DOG_API_KEY']})
        image_url = resp.json()[0]['url']
        img_block = {"type": "image", "image_url":image_url, "alt_text": "dog image"} 
        text_block = {"type":"section", "text": {"type":"mrkdwn", "text":"here is a dog pic"}}
        blocks = [img_block,  text_block]
        say(blocks=blocks)

    # basically it ends in cats and it has one word in between
    elif resttext.endswith(" dogs") and (not " " in resttext[:-len(" dogs")]):
        num = resttext[:-len(" dogs")]

        try:
            num = int(num)
        except ValueError:
            say(f"{num} could not be converted into an integer")
            return

        if num > 3 or num < 1:
            say(f"the number (what you've said as {num}) should be between 1 and 3")
            return

        resp = requests.get(f"https://api.thedogapi.com/v1/images/search?limit={num}", headers={"x-api-key":config['DOG_API_KEY']})
        blocks = []

        for pic in resp.json():
            image_url = pic['url']
            img_block = {"type": "image", "image_url":image_url, "alt_text": "dog image"} 
            blocks.append(img_block)

        text_block = {"type":"section", "text": {"type":"mrkdwn", "text":f"here are {num} dog pics"}}
        blocks.append(text_block)

        say(blocks=blocks)


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
