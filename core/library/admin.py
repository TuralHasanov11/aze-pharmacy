from django.contrib import admin
from library.models import Document


@admin.register(Document)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]