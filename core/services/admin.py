from django.contrib import admin
from services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "language"]
    search_fields = ["name", "language"]
    ordering = ["name"]