from typing import Optional
from dataclasses import dataclass


import requests
from bs4 import BeautifulSoup


class HabrParser:

    def __init__(self, url: str) -> None:
        self.url = url

    def _get_page_html(self) -> Optional[str]:
        """
        Парсит html-страницу
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        return None

    def _get_articles_from_html(self, html_page) -> list[BeautifulSoup]:
        """
        Достаёт с html-страницы все статьи
        """
        soup = BeautifulSoup(html_page, 'lxml')

        articles_block = soup.find('div', {'class': 'tm-articles-list'})
        article_list = articles_block.find_all(
            'article', {'class': 'tm-articles-list__item'})

        return article_list

    def _clean_articles_data(self, article_list) -> list[tuple[str]]:
        """
        Очищает данные статьи от html
        text
        """
        clean_data = []

        for article in article_list:
            link = 'https://habr.com' + \
                article.find('a', {'class': BlockClassName.link}).get('href')

            voices = article.find('span', {
                                  'class': BlockClassName.voices}).text.strip()
            views = article.find(
                'span', {'class': BlockClassName.views}).text.strip()

            bookmarks = article.find(
                'span', {'class': BlockClassName.bookmarks}).text.strip()

            comments = article.find(
                'span', {'class': BlockClassName.comments}).text.strip()

            clean_data.append({
                'link': link,
                'voices': voices,
                'views': views,
                'bookmarks':  bookmarks,
                'comments': comments
            })

        return clean_data

    def get_articles_data(self) -> list[tuple[str]]:
        """
        Возвращает список кортежей, которые содержат инфомарцию о каждой статье на странице
        """
        html_page = self._get_page_html()
        articles = self._get_articles_from_html(html_page)
        data = self._clean_articles_data(articles)

        return data


@dataclass(frozen=True)
class BlockClassName:

    link: str = 'tm-article-snippet__title-link'

    voices: str = 'tm-votes-meter__value tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating'

    views: str = 'tm-icon-counter__value'

    bookmarks: str = 'bookmarks-button__counter'

    comments: str = 'tm-article-comments-counter-link__value'


if __name__ == '__main__':
    parser = HabrParser('https://habr.com/ru/top/weekly/')
    data = parser.get_articles_data()

    for i in (data):
        print(i)
