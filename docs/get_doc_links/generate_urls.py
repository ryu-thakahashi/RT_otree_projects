from pathlib import Path

WD_PATH = Path(__file__).resolve().parent

def read_extracted_links():
    with open(WD_PATH / "extracted_links.txt", "r") as f:
        links = f.readlines()
    return links

def concat_links():
    links = read_extracted_links()
    BASE_URL = "https://otree.readthedocs.io/ja/latest/"
    with open(WD_PATH / "res_links.txt", "w") as f:
        for link in links:
            f.write(BASE_URL + link)

if __name__ == "__main__":
    concat_links()