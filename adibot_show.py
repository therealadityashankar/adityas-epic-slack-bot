from config import config
from block_helper import create_img_block, create_markdown_block
import requests


def adibot_show_service(message, say, words):
    if len(words) == 2:
        github_url = config['github']
        say("to see a list of options of what adi-bot can" + "show, see" + github_url)

    elif len(words) == 3:
        if words[-1] == "cat":
            url = get_cat_images(1)[0]["url"]
            alt = "cat image"
            ftext = "here is a cat pic"

        elif words[-1] == "dog":
            url = get_dog_images(1)[0]["url"]
            alt = "dog image"
            ftext = "here is a dog pic"

        else:
            return

        blocks = [
            create_img_block(url, alt),
            create_markdown_block(ftext),
        ]
        say(blocks=blocks)

    # basically it ends in cats and it has one word in between
    elif len(words) == 4:
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

        else:
            return

        blocks = [create_img_block(pic["url"], alt) for pic in images]
        blocks.append(create_markdown_block(text))
        say(blocks=blocks)

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
