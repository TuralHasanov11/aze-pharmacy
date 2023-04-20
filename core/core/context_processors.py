import os


def config(request):
    return {
        "config": {
            "app": {
                "name": os.environ.get("APP_NAME", ""),
                "site_url": os.environ.get("SITE_URL", "")
            },
        }
    }
