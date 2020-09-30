import argparse
import time
import ctypes


from app.common import (
    SPI_SET_DESKTOP_WALLPAPER,
    SPIF_SEND_WIN_INI_CHANGE,
    SPIF_UPDATE_INI_FILE,
    save_img,
)


def parse_args() -> argparse.Namespace:
    """Pars arguments from user or use default args."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--interval",
        default=5,
        type=int,
        help="Refresh interval in minutes. Default is 5 minutes.",
    )
    parser.add_argument(
        "-q",
        "--query",
        default="sport",
        help="choose a wallpaper theme default sport",
    )
    namespace = parser.parse_args()
    return namespace


def validate_args(args: argparse.Namespace) -> None:
    """Check interval according to API requirements"""
    if args.interval < 2:
        raise ValueError(
            "interval can not be less than 2 minutes because of API requirements."
        )


def choose_background(query) -> str:
    """Download random image, save to images and return path to the image."""
    # maximum 50 requests per hour
    path = save_img(query)
    return path


def refresh_background(interval, query):
    while True:
        path = choose_background(query)
        set_background(path)
        time.sleep(interval)


def set_background(path: str):
    """Change background depending on bit size"""
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SET_DESKTOP_WALLPAPER,
        0,
        path,
        SPIF_SEND_WIN_INI_CHANGE | SPIF_UPDATE_INI_FILE,
    )


def main():
    args = parse_args()
    try:
        validate_args(args)
        interval = args.interval * 60  # convert minutes to seconds
        query = args.query
        refresh_background(interval, query)
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print("Error: {}".format(err))
        raise


if __name__ == "__main__":
    main()
