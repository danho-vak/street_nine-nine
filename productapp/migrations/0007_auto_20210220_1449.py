# Generated by Django 3.1.4 on 2021-02-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0006_auto_20210217_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_origin_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sale_price',
            field=models.PositiveIntegerField(),
        ),
    ]
