# Generated by Django 4.1.7 on 2023-05-28 13:20

from django.db import migrations, models
import django.utils.timezone
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='/static/images/main/products/default.png', upload_to=store.models.product_image_path),
        ),
    ]
