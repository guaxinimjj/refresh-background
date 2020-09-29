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
        "-i", "--interval", default=10, type=int, help="Refresh interval in minutes."
    )
    return parser.parse_args()


def validate_args(args):
    """Check."""
    ...


def choose_background() -> str:
    """Download random image, save to images and return path to the image."""
    # maximum 50 requests per hour
    path = save_img()
    return path


def refresh_background(interval):
    while True:
        path = choose_background()
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
    validate_args(args)
    interval = args.interval * 60  # convert minutes to seconds
    try:
        refresh_background(interval)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
