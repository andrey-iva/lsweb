# Generated by Django 4.0.4 on 2022-05-07 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0045_alter_post_body_preview_alter_post_image_preview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
    ]