# Generated by Django 4.0.4 on 2022-04-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_alter_product_name_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=300, verbose_name='Слаг'),
        ),
    ]
