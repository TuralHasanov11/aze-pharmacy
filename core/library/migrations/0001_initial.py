# Generated by Django 4.1.7 on 2023-04-05 09:01

import django.core.validators
from django.db import migrations, models
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('file', models.FileField(upload_to=library.models.document_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'mp4', 'pptx', 'ppt', 'pptm', 'mov', 'webm'])])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
