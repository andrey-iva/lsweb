# Generated by Django 4.0.4 on 2022-06-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0063_alter_product_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video_shot',
            field=models.ImageField(blank=True, upload_to='video/shot/%Y/%m/%d', verbose_name='Заставка для видео'),
        ),
    ]