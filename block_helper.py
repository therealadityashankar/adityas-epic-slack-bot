def create_img_block(url, alt):
    return {"type": "image", "image_url": url, "alt_text": alt}


def create_markdown_block(text):
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


