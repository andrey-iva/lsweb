# Generated by Django 4.0.4 on 2022-04-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_product_full_url_alter_product_image_base_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name_plural': 'Дополнительные изображения'},
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(db_index=True, max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, verbose_name='Слаг'),
        ),
    ]