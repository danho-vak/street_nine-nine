# Generated by Django 3.1.4 on 2021-01-08 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0004_auto_20210108_1706'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductDetailImages',
            new_name='ProductDetailImage',
        ),
        migrations.RenameModel(
            old_name='ProductThumbnailImages',
            new_name='ProductThumbnailImage',
        ),
    ]