# Generated by Django 4.0.4 on 2022-04-30 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_alter_post_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand_car',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Марка машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_number',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_car',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Модель машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_install',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена установки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Тип (товар/услуга)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seat_type',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Тип сиденья'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Год выпуска'),
        ),
    ]