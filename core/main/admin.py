from django.contrib import admin
from main.models import Company, Question, SiteInfo, SiteText


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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question"]
    search_fields = ["question", "answer"]
    ordering = ["question"]