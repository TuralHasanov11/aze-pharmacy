# Generated by Django 4.1.7 on 2023-04-09 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('EDITOR', 'Editor'), ('OPERATOR', 'Operator'), ('STAFF', 'Staff')], default='STAFF', max_length=50),
        ),
    ]