# Generated by Django 4.1.7 on 2023-05-10 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_status',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('FAILED', 'Failed')], default='PENDING', max_length=20),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.CreateModel(
            name='OrderDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_status', models.CharField(choices=[('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('FAILED_DELIVERY', 'Failed Delivery'), ('RETURNED', 'Returned'), ('CANCELLED', 'Cancelled')], default='PROCESSING', max_length=30)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('courier_name', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_delivery', to='orders.order')),
            ],
        ),
    ]