from django.db.models import F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main.models import SiteInfo
from store.models import Category


def build_tree(objects):
    container = [{"route": obj.get_absolute_url, "title": obj.name, "parent_id": obj.parent_id, "id": obj.id} for obj in objects]
    id_map = {obj["id"]: obj for obj in container}
    roots = []

    for obj in container:
        parent_id = obj["parent_id"]
        if parent_id is None:
            roots.append(obj)
        else:
            parent = id_map.get(parent_id)
            if 'children' not in parent:
                parent['children'] = []
            parent['children'].append(obj)
    return roots


def default_menu(request):
    categories = Category.objects.all().only('id', 'parent_id', 'name').order_by(
        'level', F('parent_id').desc(nulls_last=False))

    return {
        "default_menu": [
            {"title": _("Home"), "route": reverse("main:index")},
            {"title": _("Library"), "route": reverse("library:index")},
            {"title": _("News"), "route": reverse("news:index")},
            {"title": _("Services"), "route": reverse("services:index")},
            {"title": _("Shop"), "route": reverse("store:products"),
                "children": build_tree(categories)
             },
            {"title": _("About Us"), "route": reverse("main:about")},
            {"title": _("Career"), "route": reverse("main:career")},
            {"title": _("Contact Us"), "route": reverse("main:contact")},
        ]
    }


def default_footer_menu(request):
    return {
        "default_footer_menu": {
            "services": [
                {"title": _("Services"), "route": "services:index"},
                {"title": _("Shop"), "route": "store:products"},
                {"title": _("Career"), "route": "main:career"},
            ],
            "support": [
                {"title": _("Library"), "route": "library:index"},
                {"title": _("News"), "route": "news:index"},
                {"title": _("Contact Us"), "route": "main:contact"},
                {"title": _("FAQ"), "route": "main:faq"},
            ],
            "company_information": [
                {"title": _("About Us"), "route": "main:about"},
                {"title": _("Terms and Conditions"),
                 "route": "main:terms-and-conditions"},
                {"title": _("Privacy Policy"), "route": "main:privacy-policy"},
                {"title": _("Return Policy"), "route": "main:return-policy"},
            ]
        }
    }


def site_info(request):
    siteInfo = SiteInfo.objects.only(
        "phone", "address", "email", "facebook_link", "twitter_link", "instagram_link", "youtube_link", "tiktok_link").first()
    if siteInfo:
        return {
            "site_info": {
                "phone": siteInfo.phone,
                "address": siteInfo.address,
                "email": siteInfo.email,
                "breadcrumb_image": siteInfo.breadcrumb_image.url,
                "banner_image": siteInfo.banner_image.url,
                "social_links": [
                    {"link": siteInfo.facebook_link, "icon": "fab fa-facebook"},
                    {"link": siteInfo.twitter_link, "icon": "fab fa-twitter"},
                    {"link": siteInfo.instagram_link, "icon": "fab fa-instagram"},
                    {"link": siteInfo.youtube_link, "icon": "fab fa-youtube"},
                    {"link": siteInfo.tiktok_link, "icon": "fab fa-tiktok"},
                ]
            }
        }
    return {
        "site_info": {
            "phone": "",
            "address": "",
            "email": "",
            "breadcrumb_image": "",
            "banner_image": "",
            "social_links": []
        }
    }
