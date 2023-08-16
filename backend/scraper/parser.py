from bs4 import BeautifulSoup as soup
from requests import get
from api.models import BookmarkModel
import logging

log = logging.getLogger(__name__)


def fetch_bookmark_data(url):
    resp = get(url, timeout=80)
    resp.raise_for_status()

    return resp.text


def get_title(source) -> str:
    title = ""
    try:
        title = source.find("meta", {"property": "og:title"})["content"]
    except Exception as e:
        print(f"Unable to fetch title from og: {e}")
        try:
            title = source.find("title").text
        except Exception as e:
            print(f"Unable to fetch title from 'title' tag: {e}")

    return title


def get_description(source) -> str:
    description = ""
    try:
        description = source.find("meta", {"property": "og:description"})["content"]
    except Exception as e:
        print(f"Unable to fetch description from og: {e}")
        try:
            description = source.find("meta", {"name": "description"})["content"]
        except Exception as e:
            print(f"Unable to fetch description from meta description: {e}")

    return description


def _url_type_in_list(data: str) -> str:
    return data in dict(BookmarkModel.WEBSITE_CHOICES).keys()


def get_url_type(source) -> str:
    url_type = None

    try:
        raw_type = source.find("meta", {"property": "og:type"})["content"]
    except Exception as e:
        print(f"Unable to fetch type from og: {e}")
    else:
        if _url_type_in_list(raw_type):
            url_type = raw_type
        else:
            raw_type = raw_type.split(".")[0]
            if _url_type_in_list(raw_type):
                url_type = raw_type

    if url_type is None:
        url_type = BookmarkModel.WEBSITE

    return url_type


def get_image(source) -> str:
    img = ""

    try:
        img = source.find("meta", {"property": "og:image"})["content"]
    except Exception as e:
        print(f"Unable to fetch image from og: {e}")

    return img


def parse(html: str) -> dict:
    data = {}

    html = soup(html, "html.parser")

    data["title"] = get_title(html)
    data["description"] = get_description(html)
    data["url_type"] = get_url_type(html)
    data["image"] = get_image(html)

    return data


def process_bookmark(bookmark: BookmarkModel, save: bool = False):
    html = fetch_bookmark_data(bookmark.url)
    data = parse(html)

    update_fields = ("title", "description", "url_type", "image")

    for field in update_fields:
        setattr(bookmark, field, data[field])

    if save:
        bookmark.save(update_fields=update_fields)
