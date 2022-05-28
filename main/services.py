from enum import Enum
from typing import NamedTuple

from django.utils import timezone

import requests
from bs4 import BeautifulSoup


class MonthYearTuple(NamedTuple):
    month_number: int
    year: int


def _get_current_month_and_year() -> MonthYearTuple:
    """
    Возвращает текущий год и месяц
    """
    today = timezone.now()
    month_number = today.month
    year = today.year

    return MonthYearTuple(month_number=month_number, year=year)


class ArticleTuple(NamedTuple):
    link: str
    voices: str
    views: str
    bookmarks: str
    comments: str


class ClassName(Enum):
    LINK = 'tm-article-snippet__title-link'
    VOICES = 'tm-votes-meter__value tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating'
    VIEWS = 'tm-icon-counter__value'
    BOOKMARKS = 'bookmarks-button__counter'
    COMMENTS = 'tm-article-comments-counter-link__value'


class HabrParser:

    def __init__(self, url: str) -> None:
        self.url = url

    def _get_page_html(self) -> str | None:
        """
        Парсит html-страницу
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        return None

    def _get_articles_from_html(self, html_page: str) -> list[BeautifulSoup]:
        """
        Достаёт с html-страницы все статьи
        """
        soup = BeautifulSoup(html_page, 'lxml')

        articles_block = soup.find('div', {'class': 'tm-articles-list'})
        article_list = articles_block.find_all(
            'article', {'class': 'tm-articles-list__item'})

        return article_list

    def _clean_articles_data(self, article_list) -> list[ArticleTuple]:
        """
        Очищает данные статьи от html
        text
        """
        clean_data = []

        for article in article_list:
            try:
                article_data = self._parse_article(article)
            except ValueError:
                print(article.find('h2').text)
            else:
                clean_data.append(article_data)

        return clean_data

    def _parse_article(self, article: BeautifulSoup) -> ArticleTuple:
        """
        Парсит данные из статьи
        """
        try:
            link = 'https://habr.com' + \
                article.find('a', {'class': ClassName.LINK.value}).get('href')

            voices = article.find('span', {
                'class': ClassName.VOICES.value}).text.strip()
            views = article.find(
                'span', {'class': ClassName.VIEWS.value}).text.strip()

            bookmarks = article.find(
                'span', {'class': ClassName.BOOKMARKS.value}).text.strip()

            comments = article.find(
                'span', {'class': ClassName.COMMENTS.value}).text.strip()
        except:
            raise ValueError('Это не статья')
        else:
            article = ArticleTuple(link=link, voices=voices,
                                   views=views, bookmarks=bookmarks, comments=comments)
            return article

    def get_articles_data(self) -> list[ArticleTuple] | None:
        """
        Возвращает список кортежей, которые содержат инфомарцию о каждой статье на странице
        """
        html_page = self._get_page_html()
        if html_page:
            articles = self._get_articles_from_html(html_page)
            data = self._clean_articles_data(articles)
            return data
        return None


if __name__ == '__main__':
    parser = HabrParser('https://habr.com/ru/top/daily/')
    data = parser.get_articles_data()
    print(len(data))

# TODO тесты
# exceptions (import в if __name__ == '__main__')
