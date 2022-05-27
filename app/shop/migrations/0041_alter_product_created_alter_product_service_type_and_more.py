# Generated by Django 4.0.4 on 2022-05-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0040_product_service_type_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Добавлен'),
        ),
        migrations.AlterField(
            model_name='product',
            name='service_type',
            field=models.CharField(blank=True, choices=[('установка', 'Установка'), ('разработка', 'Разработка')], max_length=20, null=True, verbose_name='Тип услуги'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Обновлен'),
        ),
    ]