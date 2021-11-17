import argparse
import json
import os
import re
import sys

import requests


def main(url, directory):
    if len(url):
        result = requests.get(url)
        if result.status_code == 200:
            match = re.search(r'<script>window.postDataJSON="(.*)"</script>', result.text)
            if match:
                if directory:
                    os.makedirs(directory)
                else:
                    directory = ""

                data = json.loads(match.group(1).replace("\\", ""))
                images = []
                is_album = False

                if len(data['media']) > 1:
                    is_album = True
                for image in data['media']:
                    images.append(image['id'] + "." + image['ext'])

                for i, image in enumerate(images):
                    result = requests.get('https://i.imgur.com/' + image)
                    if result.status_code == 200:
                        if is_album:
                            filename = '{:0>2d}_{}'.format(i + 1, image)
                        else:
                            filename = image
                        with open(os.path.join(directory, filename), 'wb') as file:
                            file.write(result.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="Full imgur url to image/gallery")
    parser.add_argument("DIR", nargs="?", help="Directory to save images")
    args = parser.parse_args()
    main(args.URL, args.DIR)
