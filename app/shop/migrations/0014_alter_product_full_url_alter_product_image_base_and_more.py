# Generated by Django 4.0.4 on 2022-04-17 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_product_brand_car_alter_product_full_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='full_url',
            field=models.CharField(blank=True, max_length=300, verbose_name='Полный URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_base',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d', verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True, verbose_name='Слаг')),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='shop.category', verbose_name='bla-bla_sub_category')),
            ],
            options={
                'verbose_name': 'Под категорию',
                'verbose_name_plural': 'Под категории',
                'ordering': ('name',),
            },
        ),
    ]