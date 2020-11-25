from config import config
from block_helper import create_img_block, create_markdown_block
import requests
import random
import urllib


def adibot_show_service(message, say, words):
    if len(words) == 2:
        github_url = config['github']
        say("to see a list of options of what adi-bot can" + "show, see" + github_url)

    elif len(words) == 3:
        word = words[-1]
        if word == "cat":
            url = get_cat_images(1)[0]["url"]
            alt = "cat image"
            ftext = "here is a cat pic"

        elif word == "dog":
            url = get_dog_images(1)[0]["url"]
            alt = "dog image"
            ftext = "here is a dog pic"

        else:
            url = get_general_pic(word)
            alt = f"{word} pic"
            ftext = f"here is a {word} pic"
            
            if url is None:
                say(f"Could not get an image for {word}, because pixabay did not return an image")
                return
            

        blocks = [
            create_img_block(url, alt),
            create_markdown_block(ftext),
        ]
        say(blocks=blocks)

        if word not in ["cat", "dog"]:
            say("this image has been retrieved from pixabay.com")

    # basically it ends in cats and it has one word in between
    elif len(words) == 4:
        if words[-1] in ["cats", "dogs"]:
            try:
                num = int(words[-2])
            except ValueError:
                say(f"{num} could not be converted into an integer")
                return

            if num > 3 or num < 1:
                e = f"\
    the number (what you've said as {num}) should be between 1 and 3"
                say(e)
                return

            if words[-1] == "cats":
                images = get_cat_images(num)
                alt = "cat image"
                text = f"here are {num} cat pics"

            elif words[-1] == "dogs":
                images = get_dog_images(num)
                alt = "dog image"
                text = f"here are {num} dog pics"

            blocks = [create_img_block(pic["url"], alt) for pic in images]
            blocks.append(create_markdown_block(text))
            say(blocks=blocks)
        else:
            search_for = " ".join(words[2:])
            url = get_general_pic(search_for)

            if url is None:
                say(f"Could not get an image for {words[-1]}, because pixabay did not return an image")
                return

            alt = f"{words[-1]} pics"
            ftext = f"here is a {words[-1]} pic"
            blocks = [
                create_img_block(url, alt),
                create_markdown_block(ftext),
            ]
            say(blocks=blocks)
            say("this image has been retrieved from pixabay.com")
    else:
        search_for = " ".join(words[2:])
        url = get_general_pic(search_for)
        if url is None:
            say(f"Could not get an image for {words[-1]}, because pixabay did not return an image")
            return
        alt = f"{words[-1]} pics"
        ftext = f"here is a {words[-1]} pic"
        blocks = [
            create_img_block(url, alt),
            create_markdown_block(ftext),
        ]
        say(blocks=blocks)
        say("this image has been retrieved from pixabay.com")


def get_dog_images(count):
    resp = requests.get(
        f"https://api.thedogapi.com/v1/images/search?limit={count}",
        headers={"x-api-key": config["DOG_API_KEY"]},
    )
    return resp.json()


def get_cat_images(num):
    resp = requests.get(
        f"https://api.thecatapi.com/v1/images/search?limit={num}",
        headers={"x-api-key": config["CAT_API_KEY"]},
    )
    return resp.json()


def get_general_pic(pic_of):
    """
    returns a general pic of the image gotten from pixabay

    returns, dict or None
       image if the image could be retrieved, else None
    """
    params = {
        "key" : config["pixabay"],
        "q" : pic_of,
        "safesearch" : "true",
        "per_page" : 3
    }

    resp = requests.get(
        f"https://pixabay.com/api/",
        params=params
    )

    jsoned = resp.json()
    totalHits = jsoned["totalHits"]

    if totalHits == 0:
        return None

    if totalHits != 0:
        # gets a random image
        resultnum = random.randrange(totalHits)
        params = {
            "key" : config["pixabay"],
            "q" : pic_of,
            "safesearch" : "true",
            "page": resultnum//3,
            "per_page" : 3
        }

        resp = requests.get(
            f"https://pixabay.com/api/",
            params=params
        )

        jsoned = resp.json()
        return jsoned["hits"][resultnum%3]["webformatURL"]
    else:
        return None

