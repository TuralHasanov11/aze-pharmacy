import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from store.models import Product


class EntryLog(HistoricalRecords):
    history_id_field = models.UUIDField(default=uuid.uuid4)
    excluded_fields = ['created_at', 'updated_at', 'last_modified_by']
    related_name = 'history'
    cascade_delete_history = True


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        CANCELLED = "CANCELLED", _("Cancelled")
        FAILED = "FAILED", _("Failed")
        REFUNDED = "REFUNDED", _("Refunded")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{12}$')
    phone = models.CharField(validators=[phone_regex], max_length=17)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)
    total_refund = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    order_id = models.CharField(max_length=255, unique=True, null=True)
    order_key = models.CharField(max_length=255, unique=True, null=True)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    notes = models.TextField(blank=True, null=True)
    is_flagged = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    history = EntryLog()
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.full_name)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def payment_status_value(self):
        return self.get_payment_status_display

    @property
    def payment_status_color(self):
        if self.payment_status == self.PaymentStatus.PAID:
            return "success"
        elif self.payment_status == self.PaymentStatus.CANCELLED:
            return "dark"
        elif self.payment_status == self.PaymentStatus.REFUNDED:
            return "warning"
        elif self.payment_status == self.PaymentStatus.FAILED:
            return "danger"
        return "primary"

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).strftime("%d.%m.%Y %H:%M")

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).strftime("%d.%m.%Y %H:%M")

    @property
    def _history_user(self):
        return self.last_modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.last_modified_by = value


class OrderRefund(models.Model):
    order = models.ForeignKey(
        Order, related_name='refunds', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    reason = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)

    @property
    def created_date(self):
        return datetime.fromisoformat(str(self.created_at)).strftime("%d.%m.%Y %H:%M")

    @property
    def created_by_name(self):
        return str(self.created_by) if self.created_by else ""


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class OrderDelivery(models.Model):
    class DeliveryStatus(models.TextChoices):
        PROCESSING = "PROCESSING", _("Processing")
        SHIPPED = "SHIPPED", _("Shipped")
        DELIVERED = "DELIVERED", _("Delivered")
        FAILED_DELIVERY = "FAILED_DELIVERY", _("Failed Delivery")
        RETURNED = "RETURNED", _("Returned")
        CANCELLED = "CANCELLED", _("Cancelled")

    order = models.OneToOneField(
        Order, related_name='order_delivery', on_delete=models.CASCADE)
    delivery_status = models.CharField(
        max_length=30, choices=DeliveryStatus.choices, default=DeliveryStatus.PROCESSING)
    delivery_date = models.DateField(null=True, blank=True)
    courier_name = models.CharField(max_length=255, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    last_modified_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    history = EntryLog()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def updated_date(self):
        return datetime.fromisoformat(str(self.updated_at)).strftime("%d.%m.%Y %H:%M")

    @property
    def delivery_status_value(self):
        return self.get_delivery_status_display

    @property
    def last_modified_by_name(self):
        return str(self.last_modified_by)

    @property
    def _history_user(self):
        return self.last_modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.last_modified_by = value
