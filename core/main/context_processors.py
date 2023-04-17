from django.utils.translation import gettext_lazy as _


def default_menu(request):
    return {
        "default_menu": [
            {"title": _("Home"), "route": "main:index"},
            {"title": _("Admin"), "route": "administration:index"},
            {"title": _("Library"), "route": "library:index"},
            {"title": _("News"), "route": "news:index"},
            {"title": _("Services"), "route": "services:index"},
            {"title": _("Shop"), "route": "store:products"},
            {"title": _("About Us"), "route": "main:about"},
            {"title": _("Career"), "route": "main:career"},
            {"title": _("Contact Us"), "route": "main:contact"},
        ]
    }


def default_footer_menu(request):
    return {
        "default_footer_menu": {
            "services": [
                {"title": _("Services"), "route": "services:index"},
                {"title": _("Shop"), "route": "store:products"},
                {"title": _("About Us"), "route": "main:about"},
                {"title": _("Career"), "route": "main:career"},
            ],
            "support": [
                {"title": _("Library"), "route": "library:index"},
                {"title": _("News"), "route": "news:index"},
                {"title": _("Contact Us"), "route": "main:contact"},
            ]
        }
    }