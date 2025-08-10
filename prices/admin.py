from django.contrib import admin

from .models import Currency, PriceHistory


# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'provider_id', 'active')
    search_fields = ('code', 'name', 'provider_id')


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('currency', 'price', 'timestamp', 'provider')
    list_filter = ('provider',)
    search_fields = ('currency__code',)
    readonly_fields = ('timestamp',)
