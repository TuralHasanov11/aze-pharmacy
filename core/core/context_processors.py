import os

from django.utils.translation import gettext_lazy as _


def config(request):
    return {
        "config": {
            "app": {
                "name": os.environ.get("APP_NAME", ""),
                "site_url": os.environ.get("SITE_URL", "")
            },

            "contact":{
                "company_address": os.environ.get("COMPANY_ADDRESS", ""),
                "phone": os.environ.get("COMPANY_PHONE", ""),
                "email": os.environ.get("COMPANY_EMAIL", ""),
            },

            "social_links": [
                {"url": "youtube.com", "icon": "fab fa-youtube"}
            ]
        }
    }
