# Generated by Django 4.1.7 on 2023-04-04 22:12

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('link', models.URLField()),
                ('cover_image', models.ImageField(upload_to=main.models.company_cover_image_path)),
            ],
            options={
                'verbose_name_plural': 'companies',
                'ordering': ['name'],
            },
        ),
    ]
