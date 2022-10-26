from rest_framework.views import exception_handler


def custom_404exception_handler(exc, context):
    response = exception_handler(exc, context)
    if 'not_found' in str(response.data):
        response.data['detail'] = (
            'К сожалению, запрошенная информация не найдена')

    return response
