# Generated by Django 3.1.4 on 2021-01-10 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0005_auto_20210108_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcategory',
            old_name='large_category',
            new_name='category_name',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='medium_category',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='small_category',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productapp.productcategory'),
        ),
        migrations.AlterField(
            model_name='productoptionchild',
            name='p_option_parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_child', to='productapp.productoptionparent', verbose_name='p_option_parent_id'),
        ),
    ]