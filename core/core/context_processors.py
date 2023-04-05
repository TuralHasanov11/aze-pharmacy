from django.utils.translation import gettext_lazy as _


def default_menu(request):
    return {
        "default_menu": [
            {"title": "Home", "route": "main:index"},
            {"title": "Admin", "route": "administration:index"},
            {"title": "DJ Admin", "route": "admin:index"},
            {"title": "Library", "route": "library:index"},
            {"title": "News", "route": "news:index"},
            {"title": "Services", "route": "services:index"},
            {"title": "Shop", "route": "store:index"},
            {"title": "About Us", "route": "main:about"},
            {"title": "Career", "route": "main:career"},
            {"title": "Contact Us", "route": "main:contact"},
        ]
    }