from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
import json

class CSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #print(request.data)
        request._dont_enforce_csrf_checks = True
        print('request')
        response = self.get_response(request)
        if isinstance(response, Response):
            #response.data['gg'] = 'gg'
            print(response.data)
            print(response.cookies)
            #response.data
            #response.context_data['asda'] = "as"
            response.data = json.dumps(response.data)
        print('response...')
        return response
