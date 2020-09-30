import pathlib
import os

import dotenv
import requests

dotenv.load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

ROOT_PATH = pathlib.Path(__file__).parents[1]
IMAGES_PATH = ROOT_PATH / "images"

# Check paths
IMAGES_PATH.mkdir(exist_ok=True)

SPI_SET_DESKTOP_WALLPAPER = 0x0014
SPIF_UPDATE_INI_FILE = 0x01
SPIF_SEND_WIN_INI_CHANGE = 0x02


def get_img(query) -> dict:
    """Download images from Unsplash.com."""
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": query,
    }
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}

    resp = requests.get(url, params=params, headers=headers)
    return resp.json()


def save_img(query) -> str:
    """Save image and return path like str."""
    body = get_img(query)

    image_url = body["urls"]["full"]
    image_id = "{}.jpg".format(body["id"])

    response = requests.get(image_url)
    content = response.content
    image_path: pathlib.Path = IMAGES_PATH / image_id

    with open(image_path, "wb") as some_picture:
        some_picture.write(content)

    return str(image_path)
