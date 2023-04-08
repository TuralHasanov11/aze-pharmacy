from django.utils.translation import gettext_lazy as _


def default_menu(request):
    return {
        "default_menu": [
            {"title": _("Home"), "route": "main:index"},
            {"title": _("Admin"), "route": "administration:index"},
            {"title": _("DJ Admin"), "route": "admin:index"},
            {"title": _("Library"), "route": "library:index"},
            {"title": _("News"), "route": "news:index"},
            {"title": _("Services"), "route": "services:index"},
            {"title": _("Shop"), "route": "store:index"},
            {"title": _("About Us"), "route": "main:about"},
            {"title": _("Career"), "route": "main:career"},
            {"title": _("Contact Us"), "route": "main:contact"},
        ]
    }


def admin_menu(request):
    return {
        "admin_menu": [
            {
                "type": "Core",
                "title": "Dashboard", 
                "route": "administration:index"
            },
            {
                "type": "Creator",
                "children": [
                    {
                        "title": "Services",
                        "children": [
                            {"title": "Service List", "route": "administration:service-list"},
                        ]
                    },
                    {
                        "title": "Library",
                        "children": [
                            {"title": "Documents", "route": "administration:document-list"},
                        ]
                    },
                    {
                        "title": "News",
                        "children": [
                            {"title": "News List", "route": "administration:post-list"},
                            {"title": "Add News", "route": "administration:post-create"},
                        ]
                    },
                    {
                        "title": "Career",
                        "children": [
                            {"title": "Company List", "route": "administration:company-list"},
                        ]
                    },
                ]
            },
            {
                "type": "Authentication",
                "children": [
                    {
                        "title": "Users",
                        "children": [
                            {"title": "User List", "route": "administration:user-list"},
                            {"title": "Add User", "route": "administration:user-create"},
                        ]
                    },
                ]
            }
        ]
    }