# Generated by Django 4.0.4 on 2022-06-14 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0058_order_yookassa_amount_order_yookassa_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма заказа'),
        ),
    ]
