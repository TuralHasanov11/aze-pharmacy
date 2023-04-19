from django.utils.translation import gettext_lazy as _


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
            {
                "title": "Orders",
                "module_permission": "orders",
                "children": [
                    {"title": "Orders", "route": "administration:orders"},
                ]
            },
            {
                "title": _("Sayt Məlumatları"),
                "module_permission": "site_info",
                "route": "administration:site-data"
            },
        ]
    return {
        "admin_menu": [item for item in menu if ("module_permission" not in item) or ("module_permission" in item and request.user.has_module_perms(item["module_permission"]))]
    }