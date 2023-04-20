from django.utils.translation import gettext_lazy as _


def admin_menu(request):
    menu = [
            {
                "type": _("Core"),
                "title": _("Dashboard"), 
                "route": "administration:index"
            },
            {
                "title": _("Services"),
                "module_permission": "services",
                "children": [
                    {"title": _("Service List"), "route": "administration:service-list"},
                ]
            },
            {
                "title": _("Library"),
                "module_permission": "library",
                "children": [
                    {"title": _("Documents"), "route": "administration:document-list"},
                ]
            },
            {
                "title": _("News"),
                "module_permission": "news",
                "children": [
                    {"title": _("Post List"), "route": "administration:post-list"},
                    {"title": _("Add Post"), "route": "administration:post-create"},
                ]
            },
            {
                "title": _("Career"),
                "module_permission": "main",
                "children": [
                    {"title": _("Company List"), "route": "administration:company-list"},
                ]
            },
            {
                "title": _("Authentication"),
                "module_permission": "user",
                "children": [
                    {"title": _("User List"), "route": "administration:user-list"},
                    {"title": _("Add User"), "route": "administration:user-create"},
                ]
            },
            {
                "title": _("Store"),
                "module_permission": "store",
                "children": [
                    {"title": _("Categories"), "route": "administration:store-category-list"},
                    {"title": _("Products"), "route": "administration:store-product-list"},
                ]
            },
            {
                "title": _("Orders"),
                "module_permission": "orders",
                "children": [
                    {"title": _("Orders"), "route": "administration:orders"},
                ]
            },
            {
                "title": _("Site Data Management"),
                "module_permission": "site_info",
                "route": "administration:site-data"
            },
        ]
    return {
        "admin_menu": [item for item in menu if ("module_permission" not in item) or ("module_permission" in item and request.user.has_module_perms(item["module_permission"]))]
    }