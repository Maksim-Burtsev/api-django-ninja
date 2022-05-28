from typing import List

from django.db.models import F

from ninja import NinjaAPI

from main.services import HabrParser, _get_current_month_and_year
from main.models import Purchase, MonthlyCost
from main.schemas import PurchaseSchema, MonthlyCostSchema, ArticleOutput


api = NinjaAPI()


@api.get('/best_weekly_articles/',
         response=List[ArticleOutput], url_name='weekly_article')
def get_weekly_articles(request):
    """
    Лучшие статьи за неделю
    """
    parser = HabrParser('https://habr.com/ru/top/weekly/')
    data = parser.get_articles_data()
    return data


@api.get('/best_daily_articles/', response=List[ArticleOutput], url_name='daily_article')
def get_daily_articles(request):
    """
    Лучшие статьи за день 
    """
    parser = HabrParser('https://habr.com/ru/top/daily/')
    data = parser.get_articles_data()
    return data


@api.post('/add_purchase/')
def add_purchase(request, purchase: PurchaseSchema):
    """
    Добавление покупки
    """
    purchase = Purchase.objects.create(**purchase.dict())
    monthly_cost, _ = MonthlyCost.objects.get_or_create(
        month_number=purchase.month_number,
        year=purchase.year
    )
    monthly_cost.spent = F('spent') + purchase.cost
    monthly_cost.save()

    return {'detail': 'created'}


@api.get('/month_total/', response=MonthlyCostSchema)
def get_month_total(request, month_number: int, year: int):
    """
    Сумма покупок за конкретный месяц и год
    """
    return MonthlyCost.objects.get(month_number=month_number, year=year)


@api.get('/get_month_purchases/', response=List[PurchaseSchema])
def get_month_purchases(request, month_number: int = None, year: int = None):
    """
    Список покупок за месяц и год
    """
    if month_number is None and year is None:
        month_number, year = _get_current_month_and_year()
        return Purchase.objects.filter(month_number=month_number, year=year)

    result = Purchase.objects.all()
    if month_number:
        result = result.filter(month_number=month_number)
    if year:
        result = result.filter(year=year)
    return result
