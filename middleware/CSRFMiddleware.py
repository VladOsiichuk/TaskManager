from django.core.cache import cache
from django.conf import settings


class CSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #print(request.data)
        response = self.get_response(request)
        return  response
        print("FROM MIDDLEWARE")
        print(response.cookies['csrftoken'].value)
        print(response.data['csrftoken'])
        response.data['csrftoken']= response.cookies['csrftoken'].value
        return response
