from typing import List

from ninja import NinjaAPI
from ninja import Schema

from main.services import HabrParser


api = NinjaAPI()


class ArticleOutput(Schema):
    link: str
    voices: str
    views: str
    bookmarks: int
    comments: int


@api.get('/best_weekly_articles/', response=List[ArticleOutput], url_name='weekly_article')
def get_weekly_articles(request):
    parser = HabrParser('https://habr.com/ru/top/weekly/')
    data = parser.get_articles_data()
    return data


@api.get('/best_daily_articles/', response=List[ArticleOutput], url_name='daily_article')
def get_daily_articles(request):
    parser = HabrParser('https://habr.com/ru/top/daily/')
    data = parser.get_articles_data()
    return data
