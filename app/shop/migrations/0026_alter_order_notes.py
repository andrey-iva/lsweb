# Generated by Django 4.0.4 on 2022-04-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_alter_order_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]