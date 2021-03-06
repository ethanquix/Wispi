import json
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

import config


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def getImageUrl(query):
    try:
        query = urllib.parse.quote(query)
        url = "https://api.qwant.com/api/search/images?count=1&offset=1&q=" + query
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/43.0.2357.134 Safari/537.36 "
        }
        soup = get_soup(url, header)
        out = json.loads(soup.__str__())["data"]["result"]["items"][0]["media"]
        return out # pragma: no cover
    except Exception as e:
        return config.DEFAULT_IMG


if __name__ == '__main__': # pragma: no cover
    print(getImageUrl("Shake ponk"))
