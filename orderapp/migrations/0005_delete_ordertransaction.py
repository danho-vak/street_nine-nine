# Generated by Django 3.1.4 on 2021-02-02 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0004_ordertransaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderTransaction',
        ),
    ]
