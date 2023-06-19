from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")
        query = request.META.get('QUERY_STRING', "")

        if settings.MAINTENANCE_BYPASS_QUERY in query:
            request.session['bypass_maintenance'] = True

        if not request.session.get('bypass_maintenance', False):
            if settings.MAINTENANCE_MODE and path != reverse("main:maintenance"):
                response = redirect(reverse("main:maintenance"))
                return response

        response = self.get_response(request)

        return response
