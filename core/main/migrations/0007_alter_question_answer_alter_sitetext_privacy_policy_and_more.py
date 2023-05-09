# Generated by Django 4.1.7 on 2023-05-09 20:23

from django.db import migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_question_alter_sitetext_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=main.models.RichTextEditorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitetext',
            name='privacy_policy',
            field=main.models.RichTextEditorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitetext',
            name='return_policy',
            field=main.models.RichTextEditorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sitetext',
            name='terms_and_conditions',
            field=main.models.RichTextEditorField(blank=True, null=True),
        ),
    ]
