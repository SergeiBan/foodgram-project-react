from rest_framework.views import exception_handler


def custom404_exception(exc, context):
    response = exception_handler(exc, context)
    if 'not_found' in str(response.data):
        response.data['detail'] = (
            'К сожалению, запрошенная информация не найдена')

    return response
