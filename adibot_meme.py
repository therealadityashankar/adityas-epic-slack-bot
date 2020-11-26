from google.cloud import storage
from config import config
from meme_maker_9000.meme import create_meme

import random
import string
import html
import json
import yaml
import os

with open("./meme_maker_9000/memes.yaml") as f:
    meme_formats = yaml.safe_load(f)
    memes_by_id = {}
    for i, (fn, item) in enumerate(meme_formats.items()):
        memes_by_id[item["identifier"]] = item
        memes_by_id[item["identifier"].lower()] = item
        memes_by_id[str(i)] = item

def adibot_meme_service(message, say, words):
    if len(words) == 2:
        say(f"see {config['github']} for how to use the meme-bot")
        return
    text = message["text"]
    meme_id = words[2]
    storage_client = storage.Client()
    bucket_name = "adi-bot-bucket"
    text_strs = text.split("|")[1:]

    if len(text_strs) == 0:
        say(f"You've not added any text input for the meme !, see {config['github']} for how to properly use this service !")
        return

    if text_strs[-1] == "": text_strs.pop()
    bucket = storage_client.get_bucket(bucket_name)

    # check if meme-id exists or not
    if not meme_id in memes_by_id:
        say(f"Could you check if you wrote the meme name correctly ?, see https://github.com/therealadityashankar/meme-maker-9000/blob/main/meme-samples.md for all possible meme names, there is no format called {meme_id}")
        return

    meme = memes_by_id[meme_id]
    texts_req = len(meme["text_points"])

    if not len(text_strs) == texts_req:
        say(f"Text strs length mismatch !, we need {texts_req} texts, you've provided us with {len(text_strs)} texts")

    _rand_id = ""
    randomer = random.SystemRandom()
    for i in range(20): _rand_id += randomer.choice(string.digits)
    filepath = f"/tmp/meme-{_rand_id}.jpg"
    correct_meme_id = meme["identifier"]
    text_strs = [html.unescape(t) for t in text_strs]
    create_meme(correct_meme_id, text_strs, filepath)
    blob = bucket.blob(f"memes/meme-{_rand_id}.jpg")
    blob.upload_from_filename(filepath)
    blob.make_public()
    os.remove(filepath)
    say(blob.public_url)


