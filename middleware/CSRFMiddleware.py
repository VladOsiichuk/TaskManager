from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
import json


class CSRF:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            domain = request.META["HTTP_ORIGIN"]
        except KeyError:
            domain = request.META['HTTP_HOST']
        except KeyError:
            domain = None

        if domain in settings.CSRF_TRUSTED_ORIGINS:
            request._dont_enforce_csrf_checks = True
        response = self.get_response(request)
        return response
