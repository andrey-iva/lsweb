# Generated by Django 4.0.4 on 2022-06-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0062_remove_product_full_url_product_video_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='video',
            field=models.FileField(blank=True, upload_to='video/%Y/%m/%d', verbose_name='Видео'),
        ),
    ]
