# Generated by Django 4.0.4 on 2022-07-23 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0074_alter_config_options_remove_config_cdek_percent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Config',
        ),
    ]
