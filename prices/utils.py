from rest_framework.response import Response


def api_response(success: bool, status_code: int, data, message: str = ''):
    return Response({
        'success': success,
        'status': status_code,
        'data': data,
        'message': message,
    }, status=status_code)
