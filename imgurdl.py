import argparse
import json
import logging
import os
import re
from typing import Optional, Tuple

import requests

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_images_data(url: str) -> Optional[dict]:
    logger.info("Downloading images data")
    try:
        result = requests.get(url)
        if result.status_code == 200:
            match = re.search(
                r'<script>window.postDataJSON="(.*)"</script>', result.text
            )
            if match:
                return json.loads(match.group(1).replace("\\", ""))
    except Exception as ex:
        logger.error("Can't get gallery data: %s", ex)
    return None


def create_images_list(data: dict) -> Tuple[list, bool]:
    images = []
    is_album = False

    if len(data["media"]) > 1:
        is_album = True
    for image in data["media"]:
        images.append(image["id"] + "." + image["ext"])
    logger.info("Found %s image(s)", len(images))

    return images, is_album


def download_images(images: list, directory: str, is_album: bool) -> None:
    for i, image in enumerate(images):
        logger.info("Downloading image %s", i + 1)
        result = requests.get("https://i.imgur.com/" + image)
        if result.status_code == 200:
            if is_album:
                filename = "{:0>2d}_{}".format(i + 1, image)
            else:
                filename = image
            with open(os.path.join(directory, filename), "wb") as file:
                file.write(result.content)


def create_directory(directory: Optional[str]) -> str:
    if directory:
        try:
            os.makedirs(directory)
        except OSError as ex:
            logger.error("Can't create a directory: %s", ex)
            exit(1)
    else:
        directory = ""
    return directory


def main(url: str, directory: Optional[str]) -> None:
    data = get_images_data(url)
    if data:
        directory = create_directory(directory)
        images, is_album = create_images_list(data)
        download_images(images, directory, is_album)
        logger.info("Done")
    else:
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="Full imgur url to image/gallery")
    parser.add_argument("DIR", nargs="?", help="Directory to save images")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel("INFO")
    main(args.URL, args.DIR)
