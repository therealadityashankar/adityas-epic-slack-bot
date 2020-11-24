from google.cloud import storage
from config import config
from meme_maker_9000.meme import create_meme

import random
import string
import json
import os

with open("./meme_maker_9000/memes.json") as f:
    meme_formats = json.load(f)
    memes_by_id = {}
    for fn, meme in meme_formats.items():
        memes_by_id[meme["identifier"]] = meme

def adibot_meme_service(message, say, words):
    if len(words) == 2:
        say(f"see {config['github']} for how to use the meme-bot")
        return
    text = message["text"]
    meme_id = words[2]
    storage_client = storage.Client()
    bucket_name = "adi-bot-bucket"
    text_strs = text.split("|")[1:]
    if text_strs[-1] == "": text_strs.pop()
    bucket = storage_client.get_bucket(bucket_name)

    # check if meme-id exists or not
    if not meme_id in memes_by_id:
        say(f"Could you check if you wrote the meme name correctly ?, see https://github.com/therealadityashankar/meme-maker-9000/blob/main/meme-samples.md for all possible meme names, there is no format called {meme_id}")
        return

    texts_req = len(memes_by_id[meme_id]["text_points"])

    if not len(text_strs) == texts_req:
        say(f"Text strs length mismatch !, we need {texts_req} texts, you've provided us with {len(text_strs)} texts")

    _rand_id = ""
    randomer = random.SystemRandom()
    for i in range(20): _rand_id += randomer.choice(string.digits)
    filepath = f"/tmp/meme-{_rand_id}.jpg"
    create_meme(meme_id, text_strs, filepath)
    blob = bucket.blob(f"/memes/meme-{_rand_id}.jpg")
    blob.upload_from_filename(filepath)
    blob.make_public()
    os.remove(filepath)
    say("This is a beta product and a WIP, I understand its complexity for now")
    say(blob.public_url)


