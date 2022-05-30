from time import time
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse_lazy

from main.models import MonthlyCost, Purchase


class ArticlesTestCase(TestCase):

    def test_weekly_articles(self):

        response = self.client.get(reverse_lazy("api-1.0.0:weekly_article"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(len(response.json()), [19, 20])

    def test_daily_articles(self):

        response = self.client.get(reverse_lazy("api-1.0.0:daily_article"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(len(response.json()), [19, 20])

    def test_get_month_total_no_args(self):

        today = timezone.now().date()
        MonthlyCost.objects.create(
            month_number=today.month,
            year=today.year,
            spent=1234567
        )

        response = self.client.get(reverse_lazy('api-1.0.0:month_total'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['spent'], 1234567)

    def test_get_month_total(self):
        today = timezone.now().date()
        MonthlyCost.objects.create(
            month_number=today.month,
            year=today.year,
            spent=1234567
        )

        response = self.client.get(
            f"{reverse_lazy('api-1.0.0:month_total')}?month_number={today.month}&year={today.year}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['spent'],  1234567)

    def test_month_purchases_no_args(self):
        today = timezone.now().date()

        for i in range(10):
            Purchase.objects.create(
                name=f'test{i}',
                cost=2**i,
                bought_at=today
            )

        response = self.client.get(reverse_lazy('api-1.0.0:month_purchases'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

    def test_month_purchases(self):

        today = timezone.now().date()
        for i in range(20):
            Purchase.objects.create(
                name=f'test{i}',
                cost=2**(i+2),
                bought_at=today
            )

        response = self.client.get(
            f"{reverse_lazy('api-1.0.0:month_purchases')}?month_number={today.month}&year={today.year}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_add_purchase(self):

        response = self.client.post(reverse_lazy('api-1.0.0:add_purchase'), {
            'name': 'test',
            'cost': 123,
            'bought_at': timezone.now().date()
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
                         {'name': 'Test', 'cost': 123, 'bought_at': '2022-05-30'})
