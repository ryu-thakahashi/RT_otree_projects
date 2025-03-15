from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_LINK = "https://otree.readthedocs.io/ja/latest/"

def get_links():
    response = requests.get(BASE_LINK)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a"):
        link = a.get("href")
        links.append(link)
    return links

def write_links():
    links = get_links()
    WD_PATH = Path(__file__).resolve().parent
    with open(WD_PATH / "links.txt", "w") as f:
        for link in links:
            f.write(link + "\n")

if __name__ == "__main__":
    # links = get_links()
    # print(links)
    write_links()