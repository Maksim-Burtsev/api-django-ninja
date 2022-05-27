from ninja import Schema
from ninja import ModelSchema

from main.models import MonthlyCost, Purchase


class ArticleOutput(Schema):
    link: str
    voices: str
    views: str
    bookmarks: int
    comments: int


class PurchaseSchema(ModelSchema):
    class Config:
        model = Purchase
        model_fields = ['name', 'cost', 'bought_at']


class MonthlyCostSchema(ModelSchema):
    class Config:
        model = MonthlyCost
        model_fields = ['month_number', 'year', 'spent']
