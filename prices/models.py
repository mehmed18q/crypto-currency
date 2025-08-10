from django.db import models


# Create your models here.
class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g. BTC
    name = models.CharField(max_length=100, blank=True)
    provider_id = models.CharField(max_length=200, blank=True, null=True)  # provider-specific id (e.g. 'bitcoin')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class PriceHistory(models.Model):
    currency = models.ForeignKey(Currency, related_name='prices', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=50)
    raw = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.currency.code} {self.price} @ {self.timestamp.isoformat()}"
