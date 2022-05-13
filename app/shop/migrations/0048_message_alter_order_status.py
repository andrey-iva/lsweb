# Generated by Django 4.0.4 on 2022-05-07 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0047_order_status_alter_order_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('subject', models.CharField(max_length=200, verbose_name='Тема сообщения')),
                ('email', models.EmailField(max_length=254)),
                ('notes', models.TextField(verbose_name='сообщение')),
                ('status', models.CharField(choices=[('no', 'Не прочитано'), ('ok', 'Прочитано')], default='new', max_length=20, verbose_name='Статус сообщения')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('proc', 'На обработке'), ('arc', 'В архиве')], default='new', max_length=20, verbose_name='Статус заказа'),
        ),
    ]
