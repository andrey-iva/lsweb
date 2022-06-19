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
        verbose_name_plural = '-Категории'

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
        help_text='Например: кронштейн, рейка, рейки, установка, разработка и.т.д. Нет необходимомти \
        вставлять текст со строницы, это будет неправильно и в таком случае лучше оставить поле пустым'
    )
    seo_desc = models.TextField(
        blank=True,
        verbose_name='SEO content',
        help_text='Нет необходимости заполнять это поле, если сюда вставлять текст со страницы, это будет \
        не правильно и в таком случае лучше оставить поле пустым'
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
        verbose_name_plural = '-Товары'
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
        verbose_name_plural = 'Дополнительные изображения'

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
    status = models.CharField(max_length=20,
                                    verbose_name='Статус',
                                    choices=(
                                        ('new', 'Новый'),
                                        ('proc', 'На обработке'),
                                        ('arc', 'В архиве')), default='new')
    yookassa_full_info = models.TextField(blank=True)
    address_full_info = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = '-Заказы'

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
        verbose_name_plural = 'обзоры'

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
        verbose_name_plural = 'сообщения'
