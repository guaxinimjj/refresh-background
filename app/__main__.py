import argparse
import random
import time
import ctypes

from .common import (
    IMAGES_PATH,
    SPI_SET_DESKTOP_WALLPAPER,
    SPIF_SEND_WIN_INI_CHANGE,
    SPIF_UPDATE_INI_FILE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--interval", default=10, type=int, help="Refresh interval in minutes."
    )
    return parser.parse_args()


def refresh_background(interval):
    while True:
        set_background()
        time.sleep(interval)


def set_background():
    """Change background depending on bit size"""
    images = list(IMAGES_PATH.iterdir())
    path = random.choice(images)

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SET_DESKTOP_WALLPAPER,
        0,
        str(path),
        SPIF_SEND_WIN_INI_CHANGE | SPIF_UPDATE_INI_FILE,
    )


def main():
    args = parse_args()
    interval = args.interval * 60  # convert minutes to seconds
    try:
        refresh_background(interval)
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print("Unhandled exception: {}".format(err))
        raise
    else:
        print('bye bye')


if __name__ == "__main__":
    main()
