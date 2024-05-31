from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'error': 'Not Found',
                'status_code': response.status_code,
                'message': 'The requested resource was not found.'
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'error': 'Forbidden',
                'status_code': response.status_code,
                'message': 'You do not have permission to perform this action.'
            }

    return response
