# Generated by Django 4.1.7 on 2023-06-03 19:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_company_last_modified_by_question_last_modified_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
