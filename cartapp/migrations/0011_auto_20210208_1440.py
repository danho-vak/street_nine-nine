# Generated by Django 3.1.4 on 2021-02-08 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0010_auto_20210208_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_option_1',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_option_2',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
