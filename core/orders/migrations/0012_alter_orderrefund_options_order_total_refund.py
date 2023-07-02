# Generated by Django 4.1.7 on 2023-05-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_payment_status_orderrefund'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderrefund',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='order',
            name='total_refund',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
