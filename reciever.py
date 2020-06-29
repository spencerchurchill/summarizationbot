from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import json

from summarize import sum_urls


def _search(query):
    r = urlopen("https://duckduckgo.com/html/?q=" +
                urllib.parse.quote_plus(query) + "&t=Summer").read()
    soup = BeautifulSoup(r, features="html.parser")
    page = soup.find_all('a', attrs={"class": "result__a"}, href=True)

    res = 3

    links = []
    for link in page[:res]:  # Return top res search results
        url = link["href"]
        o = urllib.parse.urlparse(url)
        d = urllib.parse.parse_qs(o.query)
        links.append(d["uddg"][0])

    return links


def _url_check(query):
    return urllib.parse.urlparse(query).scheme


def return_summary(query):
    urls = _search(query)
    summary = sum_urls(urls)

    return summary
