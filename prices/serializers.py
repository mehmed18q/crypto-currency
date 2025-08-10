from rest_framework import serializers

from .models import Currency, PriceHistory


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'name', 'provider_id', 'active')


class PriceHistorySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = PriceHistory
        fields = ('id', 'currency', 'price', 'timestamp', 'provider', 'raw')
