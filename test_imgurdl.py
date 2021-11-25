import pytest

from imgurdl import create_images_list, main


def test_create_images_list_no_image():
    data = {
        "id": "c5tag8c",
        "account_id": 5110584,
        "title": "I knew it! :D",
        "description": "",
        "image_count": 1,
        "in_most_viral": True,
        "is_album": True,
        "is_mature": False,
        "cover_id": "6TiQNNj",
        "created_at": "2021-12-10T00:24:43Z",
        "url": "https://imgur.com/gallery/c5tag8c",
        "privacy": "private",
        "media": [],
        "display": [],
    }

    images, is_album = create_images_list(data)
    assert is_album is False
    assert images == []


def test_create_images_list_one_image():
    data = {
        "id": "c5tag8c",
        "title": "I knew it! :D",
        "image_count": 1,
        "is_album": True,
        "cover_id": "6TiQNNj",
        "created_at": "2021-12-10T00:24:43Z",
        "url": "https://imgur.com/gallery/c5tag8c",
        "media": [
            {
                "id": "6TiQNNj",
                "account_id": 5110584,
                "mime_type": "image/png",
                "url": "https://i.imgur.com/6TiQNNj.png",
                "ext": "png",
                "width": 942,
                "height": 832,
                "size": 1045754,
                "metadata": {
                    "title": "",
                    "description": "",
                    "is_animated": False,
                    "is_looping": False,
                    "duration": 0,
                    "has_sound": False,
                },
                "created_at": "2021-12-10T00:24:29Z",
                "updated_at": None,
            }
        ],
        "display": [],
    }

    images, is_album = create_images_list(data)
    assert is_album is False
    assert images == ["6TiQNNj.png"]


def test_create_images_list_many_images():
    data = {
        "id": "hIQMyHR",
        "title": "Art byu00A0Yusuke Murata",
        "image_count": 14,
        "is_album": True,
        "cover_id": "qTd0bH9",
        "created_at": "2021-12-10T04:29:20Z",
        "url": "https://imgur.com/gallery/hIQMyHR",
        "media": [
            {
                "id": "qTd0bH9",
                "type": "image",
                "name": "tumblr_8542c339a8f7c78714ffedae542dcb0e_11deba5f_640.png",
                "url": "https://i.imgur.com/qTd0bH9.png",
                "ext": "png",
                "created_at": "2021-12-10T04:23:52Z",
            },
            {
                "id": "Qn5kDvt",
                "type": "image",
                "name": "iT1ApOE.jpg",
                "url": "https://i.imgur.com/Qn5kDvt.jpeg",
                "ext": "jpeg",
                "created_at": "2021-12-10T04:26:01Z",
            },
            {
                "id": "UuD3z8B",
                "type": "image",
                "name": "l2pnN5n.jpg",
                "url": "https://i.imgur.com/UuD3z8B.jpeg",
                "ext": "jpeg",
                "created_at": "2021-12-10T04:25:42Z",
            },
        ],
        "display": [],
    }

    images, is_album = create_images_list(data)
    assert is_album is True
    assert images == ["qTd0bH9.png", "Qn5kDvt.jpeg", "UuD3z8B.jpeg"]


def test_main_no_data(mocker):
    mocker.patch("imgurdl.get_images_data", return_value=None)
    with pytest.raises(SystemExit) as e:
        main("https://example.com/example", None)

    assert e.type == SystemExit
    assert e.value.code == 1
