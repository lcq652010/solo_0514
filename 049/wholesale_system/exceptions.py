from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'code': response.status_code,
            'message': '请求失败',
            'errors': response.data
        }
        response.data = custom_response_data
    else:
        return Response(
            {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': '服务器内部错误',
                'errors': str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response
