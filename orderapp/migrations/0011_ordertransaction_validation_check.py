# Generated by Django 3.1.4 on 2021-02-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0010_auto_20210203_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertransaction',
            name='validation_check',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]