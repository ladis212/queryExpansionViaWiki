import nltk
import requests
from bs4 import BeautifulSoup
from queue import Queue  # class useful for distributed computing


class Article:
    def __init__(self, article_title, article_text):
        self.title = article_title
        self.text = article_text


queue = Queue(maxsize=10000)
visited = list()
articles = list()

queue.put('https://en.wikipedia.org/wiki/%22Hello%2C_World!%22_program')

while len(visited) < 100:
    link = queue.get()
    visited.append(link)
    response = None
    try:
        response = requests.get(link)
    except requests.exceptions.ConnectionError:
        print("Connection refused on ", link)
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id='firstHeading')
    if (not title.string) or title.string.startswith('File:'):
        continue
    body = soup.find(id='bodyContent')
    tags = body.find_all('a')

    text = ''
    paragraphs = soup.select('p')
    for paragraph in paragraphs[0:5]:
        text += paragraph.text

    article = Article(title.string, text)
    articles.append(article)

    for tag in tags:
        href = tag.get('href')
        if (not href) \
                or href.find('/wiki/') == -1 \
                or queue.full():
            continue
        url = 'https://en.wikipedia.org' + tag['href']
        if url in visited:
            continue
        queue.put(url)

    print('len: ', len(articles), ', article: ', article.title)

for article in articles:
    print(f'[[{article.title}]]\n' + article.text)
