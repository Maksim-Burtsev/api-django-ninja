from django.db import models


class MonthlyCost(models.Model):
    """
    Месячные расходы
    """
    month_number = models.IntegerField()
    year = models.IntegerField()
    spent = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.month_number}/{self.year} total: {self.spent} p.'

    class Meta:
        unique_together = ['month_number', 'year']


class Purchase(models.Model):
    """
    Покупка
    """
    name = models.CharField(max_length=255)
    cost = models.IntegerField()
    bought_at = models.DateField()
    month_number = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.month_number = self.bought_at.month
        self.year = self.bought_at.year
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-bought_at', ]
