import json
import os
import re
import sys

import requests


def main(args):
    if len(args):
        result = requests.get(args[0])
        if result.status_code == 200:
            match = re.search(r'<script>window.postDataJSON="(.*)"</script>', result.text)
            if match:
                directory = ''
                try:
                    os.makedirs(args[1])
                    directory = args[1]
                except IndexError:
                    pass

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
    main(sys.argv[1:])
