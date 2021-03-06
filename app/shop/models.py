from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name='Название',
        help_text='Читаемое название представленное в списке категорий')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Слаг',
                            help_text='Только: цифры, латинские символы, знаки тире и нижнего подчеркивания')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорию'
        verbose_name_plural = '5.Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')
    name = models.CharField(
        max_length=300,
        db_index=True,
        verbose_name='Название',
        help_text='Категория товара'
    )
    slug = models.SlugField(
        max_length=300,
        db_index=True,
        verbose_name='Слаг',
        help_text='Созданый слаг редактировать не рекомендуется'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара',
        blank=True, 
        default=0,
        help_text='Целые и плавающие числа'
    )
    price_install = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена установки', 
        blank=True, 
        default=0,
        help_text='Целые и плавающие числа, у типа товара как услуга и для "петли якорного крепления" должно быть установлено 0'
    )
    item_number = models.CharField(
        max_length=100,
        db_index=True, 
        verbose_name='Артикул', 
        blank=True,
        help_text='Текст'
    )
    brand_car = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Марка машины',
        blank=True,
        help_text='Текст'
    )
    model_car = models.CharField(
        max_length=100,
        db_index=True, 
        verbose_name='Модель машины', 
        blank=True,
        help_text='Текст'
    )
    year = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Год выпуска', 
        blank=True,
        help_text='Текст'
    )
    seat_type = models.CharField(
        max_length=250, 
        verbose_name='Тип сиденья', 
        blank=True,
        help_text='Текст'
    )
    product_type = models.CharField(
        max_length=20,
        verbose_name='Тип товара',
        blank=True,
        choices=(
            ('услуга', 'Услуга'),
            ('рейка', 'Рейка'),
            ('кронштейн', 'Кронштейн')),
        help_text='Выбрать из списка тип товара, если выбрана услуга необходимо выбрать тип услуги ниже'
        )
    service_type = models.CharField(
        max_length=20,
        verbose_name='Тип услуги',
        blank=True,
        choices=(
            ('установка', 'Установка'),
            ('разработка', 'Разработка')),
        help_text='Выбрать из списка тип услуги, если тип товара установлен как услуга, иначе оставить пустым'
    )

    order_type = models.CharField(
        max_length=30,
        verbose_name='RetailCRM Тип заказа',
        blank=True,
        choices=(
            ('kronshtejn', 'Кронштейн'),
            ('zamery', 'Подбор/разработка'),
            ('tretiy-ryad', 'Третий ряд'),
            ('kronshtejn-ustanovka', 'Установка'),
            ('reyka-ind', 'Рейка индив-ая'),
            ('reyka', 'Рейка станд-ая')),
        default='kronshtejn',
    )

    weight = models.IntegerField(
        blank=True, 
        default=1500,
        verbose_name='Вес товара СДЕК',
        help_text='Вес товара должен быть указан в граммах'
    )

    # box = models.CharField(
    #     max_length=20,
    #     verbose_name='Тип упаковки СДЕК',
    #     blank=True,
    #     default='WASTE_PAPER',
    #     choices=(
    #         ('CARTON_BOX_XS', 'Коробка XS (0,5 кг 17х12х9 см)'),
    #         ('CARTON_BOX_S', 'Коробка S (2 кг 21х20х11 см)'),
    #         ('CARTON_BOX_M', 'Коробка M (5 кг 33х25х15 см)'),
    #         ('CARTON_BOX_L', 'Коробка L (12 кг 34х33х26 см)'),
    #         ('CARTON_BOX_500GR', 'Коробка (0,5 кг 17х12х10 см)'),
    #         ('CARTON_BOX_1KG', 'Коробка (1 кг 24х17х10 см)'),
    #         ('CARTON_BOX_2KG', 'Коробка (2 кг 34х24х10 см)'),
    #         ('CARTON_BOX_3KG', 'Коробка (3 кг 24х24х21 см)'),
    #         ('CARTON_BOX_5KG', 'Коробка (5 кг 40х24х21 см)'),
    #         ('CARTON_BOX_10KG', 'Коробка (10 кг 40х35х28 см)'),
    #         ('CARTON_BOX_15KG', 'Коробка (15 кг 60х35х29 см)'),
    #         ('CARTON_BOX_20KG', 'Коробка (20 кг 47х40х43 см)'),
    #         ('CARTON_BOX_30KG', 'Коробка (30 кг 69х39х42 см)'),
    #         ('BUBBLE_WRAP', 'Воздушно-пузырчатая пленка'),
    #         ('WASTE_PAPER', 'Макулатурная бумага'),
    #         ('CARTON_FILLER', 'Прессованный картон "филлер" (55х14х2,3 см)'),
    #     ),
    # )

    available = models.BooleanField(
        default=True,
        verbose_name='наличие', 
        blank=True,
        help_text='Наличие товара, есть или нет'
    )

    image_base = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name='Изображение',
        help_text='Основное изображение товара'
    )
    video = models.FileField(
        upload_to='video/%Y/%m/%d',
        blank=True,
        verbose_name='Видео',
        help_text='Для видео необходим скриншот будет лучше, если загружать оптимизированное видео'
    )
    video_shot = models.ImageField(
        upload_to='video/shot/%Y/%m/%d',
        blank=True,
        verbose_name='Заставка для видео',
        help_text='Скриншот для видео, размер скриншота должен соответствовать размеру изображения\
         товара или соотношение сторон должно быть одинаковым'
    )
    frame_video = models.TextField(blank=True, default='')
    description_short = models.TextField(
        blank=True,
        verbose_name='Краткое описание')
    description_full = models.TextField(
        blank=True, 
        verbose_name='Полное описание')
    seo_title = models.TextField(
        blank=True,
        verbose_name='SEO title',
        help_text='Обязательно для заполнения'
    )
    seo_key = models.TextField(
        blank=True, 
        verbose_name='SEO keys',
    )
    seo_desc = models.TextField(
        blank=True,
        verbose_name='SEO content',
    )
    # full_url = models.TextField(
    #     blank=True, verbose_name='Полный URL')
    attribute = models.CharField(
        max_length=30,
        blank=True, 
        default='', 
        verbose_name="Атрибут",
        help_text='Поле используется для индефикации товара, в частности для "петли якорного крепления"'
    )

    # created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Добавлен')
    # updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Обновлен')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = '2.Товары'
        indexes = (
            models.Index(fields=('id', 'slug')),
        )
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                related_name='images',
                                on_delete=models.CASCADE,
                                verbose_name='Изображение')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = '6.Галерея'

    def __str__(self):
        return self.image.url


class Order(models.Model):
    policy = models.CharField(max_length=30, verbose_name='С политикой сайта')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='фамилия')
    country = models.CharField(max_length=100, blank=True, verbose_name='страна')
    region = models.CharField(max_length=100, blank=True, verbose_name='регион')
    # city = models.CharField(max_length=100, verbose_name='город')
    address = models.CharField(max_length=250, blank=True, verbose_name='адрес')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='индекс')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    email = models.EmailField(blank=True)
    delivery_type = models.CharField(max_length=100, verbose_name="доставка")
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Сумма')
    notes = models.TextField(max_length=500, blank=True,
                             verbose_name='примечание к заказу')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='оплачен')
    yookassa_id = models.CharField(max_length=200, blank=True, verbose_name='Юкасса ID транзакции')
    yookassa_amount = models.DecimalField(
            max_digits=10, decimal_places=2, verbose_name='Юкасса сумма', blank=True, default=0)
    yookassa_status = models.CharField(max_length=30, blank=True, verbose_name='Юкасса статус')
    retail_crm_status = models.CharField(max_length=30, blank=True, verbose_name='CRM_ID')
    status = models.CharField(max_length=20,
                                    verbose_name='Статус',
                                    choices=(
                                        ('new', 'Новый'),
                                        ('arc', 'В архиве')), default='new')
    yookassa_full_info = models.TextField(blank=True)
    address_full_info = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = '1.Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE,
                                verbose_name='товар')
    install = models.BooleanField(default=False, verbose_name='установка')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='цена')
    price_install = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name='цена установки')
    quantity = models.PositiveIntegerField(
        default=1, verbose_name='колличество')

    class Meta:
        verbose_name_plural = 'товары'

    def __str__(self):
        return str(self.product.item_number)

    def get_cost(self):
        return self.price * self.quantity


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Не опубликовано'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250, verbose_name='заголовок')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish',
                            verbose_name='слаг')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='автор')
    image_preview = models.ImageField(upload_to='blog_posts/%Y/%m/%d', 
                                     null=True,
                                     blank=True,
                                     verbose_name='изображение')
    body_preview = models.TextField(verbose_name='отрывок статьи')
    body = models.TextField(verbose_name='текст статьи')
    publish = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='статус')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ('publish',)
        verbose_name_plural = '3.Обзоры'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:post_detail',
                       args=[self.slug])

class Message(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    subject = models.CharField(max_length=200, verbose_name='Тема сообщения')
    email = models.EmailField()
    notes = models.TextField(verbose_name='сообщение')
    status = models.CharField(max_length=20,
                              verbose_name='Статус сообщения',
                              choices=(
                                ('no', 'Не прочитано'),
                                ('ok', 'Прочитано')), default='no')

    class Meta:
        ordering = ('status',)
        verbose_name_plural = '4.Сообщения'
