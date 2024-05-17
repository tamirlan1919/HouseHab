from rest_framework.views import exception_handler
from rest_framework.response import Response
from .exceptions import InvalidDataException, DuplicateFieldException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidDataException, DuplicateFieldException)):
        data = {'detail': exc.detail}
        if response is not None:
            response.data = data
        else:
            response = Response(data, status=exc.status_code)

    return response
