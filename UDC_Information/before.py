import requests
from bs4 import BeautifulSoup
denen_url = "https://supersolenoid.jp/blog-category-12.html"
def get_new_article():
    response = requests.get(denen_url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div",class_="EntryTitle")
    article = []
    for a in articles:
        article.append(a.find("a").get("href"))
    return article

print(get_new_article())