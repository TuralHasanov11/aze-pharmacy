# Generated by Django 4.1.7 on 2023-05-23 22:12

import django.core.validators
from django.db import migrations, models
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_document_options_document_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=library.models.document_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'mp4', 'pptx', 'ppt', 'pptm', 'mov', 'webm', 'png', 'jpg'])]),
        ),
    ]