from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    # Let DRF process the error first
    response = drf_exception_handler(exc, context)
    if response is None:
        # Unexpected internal error
        return Response({
            'success': False,
            'status': 500,
            'data': None,
            'message': str(exc),
        }, status=500)

    return Response({
        'success': False,
        'status': response.status_code,
        'data': response.data,
        'message': response.status_text,
    }, status=response.status_code)
