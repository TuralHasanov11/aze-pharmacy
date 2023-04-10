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


def admin_menu(request):
    menu = [
            {
                "type": "Core",
                "title": "Dashboard", 
                "route": "administration:index"
            },
            {
                "title": "Services",
                "module_permission": "services",
                "children": [
                    {"title": "Service List", "route": "administration:service-list"},
                ]
            },
            {
                "title": "Library",
                "module_permission": "library",
                "children": [
                    {"title": "Documents", "route": "administration:document-list"},
                ]
            },
            {
                "title": "News",
                "module_permission": "news",
                "children": [
                    {"title": "News List", "route": "administration:post-list"},
                    {"title": "Add News", "route": "administration:post-create"},
                ]
            },
            {
                "title": "Career",
                "module_permission": "main",
                "children": [
                    {"title": "Company List", "route": "administration:company-list"},
                ]
            },
            {
                "title": "Authentication",
                "module_permission": "user",
                "children": [
                    {"title": "User List", "route": "administration:user-list"},
                    {"title": "Add User", "route": "administration:user-create"},
                ]
            },
            {
                "title": "Store",
                "module_permission": "store",
                "children": [
                    {"title": "Categories", "route": "administration:store-category-list"},
                    {"title": "Products", "route": "administration:store-product-list"},
                ]
            },
        ]
    return {
        "admin_menu": [item for item in menu if "module_permission" in item and request.user.has_module_perms(item["module_permission"])]
    }