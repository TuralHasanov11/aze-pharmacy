# Generated by Django 4.1.7 on 2023-06-14 17:46

from django.db import migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_siteinfo_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitetext',
            name='order_success',
            field=main.models.RichTextEditorField(blank=True, null=True),
        ),
    ]
