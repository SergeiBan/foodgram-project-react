from rest_framework.views import exception_handler


def custom404_exception(exc, context):
    views = {
        
    }
    response = exception_handler(exc, context)
    print('recipes' in str(context['view']), context)
    response.data['detail'] = 'К сожалению, запрошенная информация не найдена'
    return response
