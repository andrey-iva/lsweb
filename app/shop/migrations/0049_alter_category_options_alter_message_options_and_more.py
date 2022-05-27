# Generated by Django 4.0.4 on 2022-05-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_message_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категорию', 'verbose_name_plural': '-Категории'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('status',), 'verbose_name_plural': 'сообщения'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created',), 'verbose_name': 'Заказ', 'verbose_name_plural': '-Заказы'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('publish',), 'verbose_name_plural': 'обзоры'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id',), 'verbose_name': 'Товар', 'verbose_name_plural': '-Товары'},
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(default='', max_length=100, verbose_name='доставка'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('no', 'Не прочитано'), ('ok', 'Прочитано')], default='no', max_length=20, verbose_name='Статус сообщения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=250, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, max_length=100, verbose_name='страна'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=100, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='индекс'),
        ),
        migrations.AlterField(
            model_name='order',
            name='region',
            field=models.CharField(blank=True, max_length=100, verbose_name='регион'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body_preview',
            field=models.TextField(verbose_name='отрывок статьи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Не опубликовано'), ('published', 'Опубликовано')], default='draft', max_length=10, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(blank=True, default=True, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand_car',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Марка машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_full',
            field=models.TextField(blank=True, verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_short',
            field=models.TextField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='full_url',
            field=models.TextField(blank=True, verbose_name='Полный URL'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_base',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_number',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_car',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Модель машины'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_install',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Цена установки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, choices=[('услуга', 'Услуга'), ('рейка', 'Рейка'), ('кронштейн', 'Кронштейн')], max_length=20, verbose_name='Тип товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seat_type',
            field=models.CharField(blank=True, max_length=250, verbose_name='Тип сиденья'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_desc',
            field=models.TextField(blank=True, verbose_name='SEO content'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_key',
            field=models.TextField(blank=True, verbose_name='SEO keys'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_title',
            field=models.TextField(blank=True, verbose_name='SEO title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='service_type',
            field=models.CharField(blank=True, choices=[('установка', 'Установка'), ('разработка', 'Разработка')], max_length=20, verbose_name='Тип услуги'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.CharField(blank=True, db_index=True, max_length=100, verbose_name='Год выпуска'),
        ),
    ]