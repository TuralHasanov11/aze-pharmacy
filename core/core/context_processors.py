import os

from django.utils.translation import gettext_lazy as _


def config(request):
    return {
        "config": {
            "app": {
                "name": os.environ.get("APP_NAME", ""),
                "site_url": os.environ.get("SITE_URL", "")
            },
        }
    }
