# Generated by Django 4.1.7 on 2023-05-30 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_rename_last_modified_by_orderrefund_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]