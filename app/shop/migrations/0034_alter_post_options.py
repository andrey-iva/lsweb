# Generated by Django 4.0.4 on 2022-04-29 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',), 'verbose_name_plural': 'статьи'},
        ),
    ]