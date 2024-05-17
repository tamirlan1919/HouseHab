from rest_framework.exceptions import APIException

class InvalidDataException(APIException):
    status_code = 401
    default_detail = 'Invalid data provided.'
    default_code = 'invalid_data'

class DuplicateFieldException(APIException):
    status_code = 402
    default_detail = 'D'
    default_code = 'duplicate_field'
