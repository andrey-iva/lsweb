# Generated by Django 4.0.4 on 2022-06-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_product_attribute_alter_order_grand_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='yookassa_id',
            field=models.CharField(blank=True, max_length=200, verbose_name='Юкасса номер транзакции'),
        ),
    ]
