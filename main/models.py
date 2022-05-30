from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class MonthlyCost(models.Model):
    """
    Месячные расходы
    """
    month_number = models.IntegerField()
    year = models.IntegerField()
    spent = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.month_number}/{self.year} total: {self.spent} p.'

    class Meta:
        unique_together = ['month_number', 'year']


def validate_bought_at(value):
    date_now = timezone.now().date()
    if value > date_now:
        raise ValidationError('Date can be in the future!')


class Purchase(models.Model):
    """
    Покупка
    """

    name = models.CharField(max_length=255)
    cost = models.IntegerField()
    bought_at = models.DateField(validators=[validate_bought_at])
    month_number = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.month_number = self.bought_at.month
        self.year = self.bought_at.year
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-bought_at', '-cost']
