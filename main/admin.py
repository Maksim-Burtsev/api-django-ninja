from django.contrib import admin

from main.models import MonthlyCost, Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_cost_with_p', 'bought_at')

    def get_cost_with_p(self, obj):
        return f'{obj.cost} p.'

    get_cost_with_p.short_description = 'cost'

@admin.register(MonthlyCost)
class MonthlyCostsAdmin(admin.ModelAdmin):
    list_display = ('month_with_year', 'spent_with_p')

    def month_with_year(self, obj):
        return f'{obj.month_number}/{obj.year}'

    def spent_with_p(self, obj):
        return f'{obj.spent} p.'

    month_with_year.short_description = 'month'
    spent_with_p.short_description = 'spent'