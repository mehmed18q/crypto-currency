from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from prices.models import Currency
from prices.serializers import PriceHistorySerializer
from prices.utils import api_response
from .tasks import fetch_prices_task


# Create your views here.

class TriggerFetchAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Add fetch prices task to queue.",
        responses={
            202: openapi.Response('Successful response')
        }
    )
    def post(self, request):
        # Run asynchronous task
        fetch_prices_task.delay()
        return Response({
            'success': True,
            'status': status.HTTP_202_ACCEPTED,
            'data': None,
            'message': 'Fetch task queued',
        }, status=status.HTTP_202_ACCEPTED)


class LatestPricesAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Return the latest prices for all active currencies.",
        responses={
            200: openapi.Response('Successful response'),
            404: 'No prices found',
        }
    )
    def get(self, request):
        currencies = Currency.objects.filter(active=True)
        result = []
        for c in currencies:
            latest_price = c.prices.order_by('-timestamp').first()
            if latest_price:
                result.append({
                    'code': c.code,
                    'price': str(latest_price.price),
                    'timestamp': latest_price.timestamp.isoformat(),
                    'provider': latest_price.provider,
                })
            else:
                result.append({
                    'code': c.code,
                    'price': None,
                    'timestamp': None,
                    'provider': None,
                })
        return api_response(True, 200, result, 'Latest prices fetched successfully')


class PriceHistoryAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Return the price history for the currency.",
        responses={
            200: openapi.Response('Successful response', PriceHistorySerializer(many=True)),
            404: 'No prices found',
        }
    )
    def get(self, request, code: str):
        limit = int(request.query_params.get('limit', 50))  # محدودیت تعداد داده‌ها
        try:
            currency = Currency.objects.get(code__iexact=code)
        except Currency.DoesNotExist:
            return api_response(False, 404, None, 'Currency not found')

        prices_qs = currency.prices.all()[:limit]
        serializer = PriceHistorySerializer(prices_qs, many=True)
        return api_response(True, 200, serializer.data, 'Price history fetched successfully')
