# Generated by Django 4.1.7 on 2023-06-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_order_last_modified_by_historicalorderdelivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded')], default='PENDING', max_length=20),
        ),
    ]
