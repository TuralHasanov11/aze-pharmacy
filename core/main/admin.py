from django.contrib import admin
from main.models import Company, SiteInfo, SiteText


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    pass