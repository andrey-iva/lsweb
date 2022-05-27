# Generated by Django 4.0.4 on 2022-04-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_product_full_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand_car',
            field=models.CharField(db_index=True, max_length=30, verbose_name='Марка машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='full_url',
            field=models.CharField(max_length=300, verbose_name='Полный URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_number',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_car',
            field=models.CharField(db_index=True, max_length=30, verbose_name='Модель машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_install',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена установки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(max_length=50, verbose_name='Тип (товар/услуга)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seat_type',
            field=models.CharField(max_length=250, verbose_name='Тип сиденья'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_desc',
            field=models.TextField(verbose_name='SEO content'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_key',
            field=models.CharField(max_length=100, verbose_name='SEO keys'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_title',
            field=models.CharField(max_length=100, verbose_name='SEO title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Год выпуска'),
        ),
    ]