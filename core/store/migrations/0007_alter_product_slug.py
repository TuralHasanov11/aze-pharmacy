# Generated by Django 4.1.7 on 2023-04-20 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_sku_alter_product_discount_alter_stock_units_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]
