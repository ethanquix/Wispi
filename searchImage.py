from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import urllib.parse
import os
import json


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def getImageUrl(query):
    query = urllib.parse.quote(query)
    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/43.0.2357.134 Safari/537.36 "
    }
    soup = get_soup(url, header)
    for tmp in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(tmp.text)["ou"], json.loads(tmp.text)["ity"]
        return (link)


if __name__ == '__main__':
    print(getImageUrl("Meatspin"))