from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
import json


class CSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(settings.CSRF_TRUSTED_ORIGINS)
        print(request.META["HTTP_REFERER"])
        if request.META["HTTP_REFERER"] in settings.CSRF_TRUSTED_ORIGINS:
            print("META WORKS!")
            request._dont_enforce_csrf_checks = True
        response = self.get_response(request)
        return response
