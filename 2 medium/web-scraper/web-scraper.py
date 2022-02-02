import os
from string import punctuation

import requests
from bs4 import BeautifulSoup

domain = "https://www.nature.com"
resource = "/nature/articles"
n_pages, article_type = (input(), input())
trans = str.maketrans(" ", "_", punctuation)

for n in range(1, int(n_pages) + 1):
    os.makedirs(f"Page_{n}", exist_ok=True)
    r = requests.get(f"{domain}{resource}", params={"year": "2020", "page": n})
    soup = BeautifulSoup(r.content, "html.parser")

    articles = [
        article
        for article in soup.find_all("article")
        if article.find("span", "c-meta__type").get_text() == article_type
    ]

    for article in articles:
        r = requests.get(f"{domain}{article.find('a')['href']}")
        soup = BeautifulSoup(r.content, "html.parser")

        path = os.path.join(f"Page_{n}", f"{soup.find('h1').text.translate(trans)}.txt")
        with open(path, "wb") as f:
            text = soup.find("div", "c-article-body").text.strip().encode()
            f.write(text)
