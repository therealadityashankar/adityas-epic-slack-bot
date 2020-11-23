import requests
from config import config
from block_helper import create_markdown_block

def adibot_make_service(message, say, words):
    if words[-1] == "becareful--joke" \
            or words[-1] == "becareful--jokes":
        if len(words) == 3:
            joke = get_jokes(1)

            if joke["error"]:
                say("there was an error getting the joke !")
                return
            say("if the joke is problamatic or has issue, please file a issue on {config['github']}, this is still a beta feature being worked")
            say(joke_to_text(joke))

        if len(words) == 4:
            try:
                num = int(words[-2])
            except ValueError:
                say(f"could not convert {words[-2]} into an integer,\
see {config['github']} how to use the function")
                return

            if num == 1:
                say(f"use `adi-bot make joke` if you just want one joke")

            if num < 2 or num > 6:
                say(f"the number of jokes, (what you've put as {num}) should be in between 2 and 6")
                return

            jokes = get_jokes(num)

            if jokes["error"]:
                say("there was an error getting the jokes !")
                return


            jokes = jokes['jokes']
            cmb = create_markdown_block
            seperator = "\n--------------------------------------------------"
            blocks = [cmb(joke_to_text(joke) + seperator) for joke in jokes]
            blocks = [cmb("here are a few jokes:")] + blocks

            say("if the joke is problamatic or has issue, please file a issue on {config['github']}, this is still a beta feature being worked")
            say(blocks=blocks)
    else:
        say(f"could not understand the command, {message['text']}, see {config['github']} for all adi-bot commands")

def get_jokes(n):
    blacklist = ["fuck"]
    joke_in_bl = True

    while joke_in_bl:
        joke_in_bl = False
        jokes = requests.get(f"https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist&amount={n}")
        text = jokes.text
        for word in blacklist:
            if word in text.lower():
                joke_in_bl = True
                continue

    return jokes.json()

def joke_to_text(joke):
    if joke["type"] == "single":
        return joke["joke"]

    elif joke["type"] == "twopart":
        return joke["setup"] + "\n.\n.\n.\n" + joke["delivery"]
