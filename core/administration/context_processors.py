from django.utils.translation import gettext_lazy as _


def admin_menu(request):
    menu = [
        {
            "title": _("Dashboard"),
            "route": "administration:index",
            "icon": "activity",
        },
        {
            "title": _("Services"),
            "module_permission": "services",
            "icon": "check-circle",
            "children": [
                {"title": _("Service List"),
                 "route": "administration:service-list"},
            ]
        },
        {
            "title": _("Library"),
            "module_permission": "library",
            "icon": "book",
            "children": [
                {"title": _("Documents"),
                 "route": "administration:document-list"},
            ]
        },
        {
            "title": _("News"),
            "module_permission": "news",
            "icon": "file-text",
            "children": [
                {"title": _("Post List"),
                 "route": "administration:post-list"},
                {"title": _("Add Post"),
                 "route": "administration:post-create"},
            ]
        },
        {
            "title": _("Career"),
            "module_permission": "main",
            "icon": "home",
            "children": [
                {"title": _("Company List"),
                 "route": "administration:company-list"},
            ]
        },
        {
            "title": _("Authentication"),
            "module_permission": "user",
            "icon": "user",
            "children": [
                {"title": _("User List"),
                 "route": "administration:user-list"},
                {"title": _("Add User"),
                 "route": "administration:user-create"},
            ]
        },
        {
            "title": _("Store"),
            "module_permission": "store",
            "icon": "shopping-cart",
            "children": [
                {"title": _("Categories"),
                 "route": "administration:store-category-list"},
                {"title": _("Products"),
                 "route": "administration:store-product-list"},
                {"title": _("Add Product"),
                 "route": "administration:store-product-create"},
            ]
        },
        {
            "title": _("Orders"),
            "module_permission": "orders",
            "icon": "list",
            "children": [
                {"title": _("Orders"), "route": "administration:order-list"},
            ]
        },
        {
            "title": _("Site Data Management"),
            "module_permission": "site_info",
            "icon": "globe",
            "children": [
                {"title": _("Info"), "route": "administration:site-info"},
                {"title": _("Texts"), "route": "administration:site-texts"},
                {"title": _("FAQ"), "route": "administration:site-faq-list"},
            ]
        },
    ]
    return {
        "admin_menu": [item for item in menu if ("module_permission" not in item) or
                       ("module_permission" in item and request.user.has_module_perms(item["module_permission"]))]
    }
