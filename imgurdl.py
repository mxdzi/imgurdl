import sys
import re
import requests
import json


def main(args):
    if len(args):
        result = requests.get(args[0])
        if result.status_code == 200:
            match = re.search(r"\n\s*image\s*:\s*({.*})", result.text)
            if match:
                for image in json.loads(match.group(1))['album_images']['images']:
                    result = requests.get('https://i.imgur.com/' + image['hash'] + image['ext'])
                    if result.status_code == 200:
                        filename = image['hash'] + image['ext']
                        with open(filename, 'wb') as file:
                            file.write(result.content)


if __name__ == "__main__":
    main(sys.argv[1:])
