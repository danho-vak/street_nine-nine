# Generated by Django 3.1.4 on 2021-01-11 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressapp', '0002_auto_20201231_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]