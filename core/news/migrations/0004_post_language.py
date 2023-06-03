# Generated by Django 4.1.7 on 2023-06-02 18:54

from django.db import migrations
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_post_last_modified_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='language',
            field=news.models.LanguageField(choices=[('az', 'Azerbaijani'), ('ru', 'Russian'), ('en', 'English')], default='az', max_length=2),
        ),
    ]