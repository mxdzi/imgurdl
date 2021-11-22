import argparse
import json
import logging
import os
import re
from typing import Optional

import requests

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_images_data(url: str) -> Optional[dict]:
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


def main(url: str, directory: str) -> None:
    data = get_images_data(url)
    if data:
        if directory:
            os.makedirs(directory)
        else:
            directory = ""

        images = []
        is_album = False

        if len(data["media"]) > 1:
            is_album = True
        for image in data["media"]:
            images.append(image["id"] + "." + image["ext"])

        for i, image in enumerate(images):
            result = requests.get("https://i.imgur.com/" + image)
            if result.status_code == 200:
                if is_album:
                    filename = "{:0>2d}_{}".format(i + 1, image)
                else:
                    filename = image
                with open(os.path.join(directory, filename), "wb") as file:
                    file.write(result.content)
    else:
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="Full imgur url to image/gallery")
    parser.add_argument("DIR", nargs="?", help="Directory to save images")
    args = parser.parse_args()
    main(args.URL, args.DIR)
