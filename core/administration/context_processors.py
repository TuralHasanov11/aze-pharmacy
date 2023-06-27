from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def admin_menu(request):
    menu = [
        {
            "title": _("Dashboard"),
            "route": reverse("administration:index"),
            "icon": "activity",
        },
        {
            "title": _("Services"),
            "module_permission": "services",
            "icon": "check-circle",
            "children": [
                {"title": _("Service List"),
                 "route": reverse("administration:service-list")},
            ]
        },
        {
            "title": _("Library"),
            "module_permission": "library",
            "icon": "book",
            "children": [
                {"title": _("Documents"),
                 "route": reverse("administration:document-list")},
            ]
        },
        {
            "title": _("News"),
            "module_permission": "news",
            "icon": "file-text",
            "children": [
                {"title": _("Post List"),
                 "route": reverse("administration:post-list")},
                {"title": _("Add Post"),
                 "route": reverse("administration:post-create")},
            ]
        },
        {
            "title": _("Career"),
            "module_permission": "main",
            "icon": "home",
            "children": [
                {"title": _("Company List"),
                 "route": reverse("administration:company-list")},
            ]
        },
        {
            "title": _("Authentication"),
            "module_permission": "user",
            "icon": "user",
            "children": [
                {"title": _("User List"),
                 "route": reverse("administration:user-list")},
                {"title": _("Add User"),
                 "route": reverse("administration:user-create")},
            ]
        },
        {
            "title": _("Store"),
            "module_permission": "store",
            "icon": "shopping-cart",
            "children": [
                {"title": _("Categories"),
                 "route": reverse("administration:store-category-list")},
                {"title": _("Products"),
                 "route": reverse("administration:store-product-list")},
                {"title": _("Add Product"),
                 "route": reverse("administration:store-product-create")},
            ]
        },
        {
            "title": _("Orders"),
            "module_permission": "orders",
            "icon": "list",
            "children": [
                {"title": _("Orders"), "route": reverse("administration:order-list")+"?status=paid"},
            ]
        },
        {
            "title": _("Site Data Management"),
            "module_permission": "main",
            "icon": "globe",
            "children": [
                {"title": _("Info"), "route": reverse("administration:site-info")},
                {"title": _("Texts"), "route": reverse("administration:site-texts")},
                {"title": _("FAQ"), "route": reverse("administration:site-faq-list")},
            ]
        },
    ]
    return {
        "admin_menu": [item for item in menu if ("module_permission" not in item) or
                       ("module_permission" in item and request.user.has_module_perms(item["module_permission"]))]
    }
