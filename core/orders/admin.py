from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ("full_name", "total_paid", "billing_status")
  ordering = ("-created_at", )
