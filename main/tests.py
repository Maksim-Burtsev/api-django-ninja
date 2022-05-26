from django.test import TestCase
from django.urls import reverse_lazy


class ArticlesTestCase(TestCase):

    def test_weekly_articles(self):

        response = self.client.get(reverse_lazy("api-1.0.0:weekly_article"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_daily_articles(self):

        response = self.client.get(reverse_lazy("api-1.0.0:daily_article"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)
