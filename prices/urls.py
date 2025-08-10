from django.urls import path

from .views import TriggerFetchAPIView, LatestPricesAPIView, PriceHistoryAPIView

urlpatterns = [
    path('fetch', TriggerFetchAPIView.as_view(), name='api_fetch_prices'),
    path('latest', LatestPricesAPIView.as_view(), name='latest_prices'),
    path('history/<str:code>', PriceHistoryAPIView.as_view(), name='price_history'),
]
