# Generated by Django 4.0.4 on 2022-05-05 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0044_post_body_preview_alter_post_image_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body_preview',
            field=models.TextField(verbose_name='начало статьи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_preview',
            field=models.ImageField(null=True, upload_to='blog_posts/%Y/%m/%d', verbose_name='изображение'),
        ),
    ]