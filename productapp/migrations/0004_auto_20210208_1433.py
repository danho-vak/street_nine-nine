# Generated by Django 3.1.4 on 2021-02-08 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0003_auto_20210124_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-product_created_at']},
        ),
        migrations.AlterField(
            model_name='productdetailimage',
            name='p_detail_image',
            field=models.ImageField(upload_to='product_detail_images'),
        ),
    ]
