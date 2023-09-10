import requests
from bs4 import BeautifulSoup as bs
from database import New

DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/news'


class Parser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
                          "Safari/537.36"
        }

        self.info = []

    def parse(self):
        session = requests.Session()
        res = session.get(f"https://uralpolit.ru/news/", headers=self.headers)

        soup = bs(res.text, "html.parser")
        ds = soup.find('section', 'project-page')
        links = ds.findAll('a')
        self.links = []
        for link in links:
            a = link.get('href')
            self.links.append(a)

        i = 0
        for link in self.links:
            session_ = requests.Session()
            res_ = session_.get(f"https://uralpolit.ru/" + link, headers=self.headers)

            soup = bs(res_.text, "html.parser")

            times = soup.find('time', itemprop='datePublished').text

            titles = soup.find('h1', 'news-article__title').text

            texts = soup.find('div', itemprop="articleBody").text

            texts = texts.replace("\n", " ")

            self.info.append(New(time=times, title=titles, text=texts))

    def get(self):
        self.parse()