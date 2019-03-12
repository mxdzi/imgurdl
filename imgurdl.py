import json
import os
import re
import sys

import requests


def main(args):
    if len(args):
        result = requests.get(args[0])
        if result.status_code == 200:
            match = re.search(r"\n\s*image\s*:\s*({.*})", result.text)
            if match:
                directory = ''
                try:
                    os.makedirs(args[1])
                    directory = args[1]
                except IndexError:
                    pass

                data = json.loads(match.group(1))
                images = []
                if 'album_images' in data:
                    for image in data['album_images']['images']:
                        images.append(image['hash'] + image['ext'])
                else:
                    images.append(data['hash'] + data['ext'])

                for image in images:
                    result = requests.get('https://i.imgur.com/' + image)
                    if result.status_code == 200:
                        filename = image
                        with open(os.path.join(directory, filename), 'wb') as file:
                            file.write(result.content)


if __name__ == "__main__":
    main(sys.argv[1:])
