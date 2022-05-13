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
        max_length=300, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=300, db_index=True, verbose_name='Слаг')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена товара', blank=True, default=0)
    price_install = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена установки', blank=True, default=0)
    item_number = models.CharField(
        max_length=100, db_index=True, verbose_name='Артикул', blank=True)
    brand_car = models.CharField(
        max_length=100, db_index=True, verbose_name='Марка машины', blank=True)
    model_car = models.CharField(
        max_length=100, db_index=True, verbose_name='Модель машины', blank=True)
    year = models.CharField(max_length=100, db_index=True,
                            verbose_name='Год выпуска', blank=True)
    seat_type = models.CharField(
        max_length=250, verbose_name='Тип сиденья', blank=True)
    product_type = models.CharField(max_length=20,
                                    verbose_name='Тип товара',
                                    blank=True,
                                    choices=(
                                        ('услуга', 'Услуга'),
                                        ('рейка', 'Рейка'),
                                        ('кронштейн', 'Кронштейн')))
    service_type = models.CharField(max_length=20,
                                    verbose_name='Тип услуги',
                                    blank=True,
                                    choices=(
                                        ('установка', 'Установка'),
                                        ('разработка', 'Разработка')))
    available = models.BooleanField(
        default=True, verbose_name='В наличии', blank=True)

    image_base = models.ImageField(upload_to='products/%Y/%m/%d',
                                   blank=True,
                                   verbose_name='Изображение')
    description_short = models.TextField(
        blank=True, verbose_name='Краткое описание')
    description_full = models.TextField(
        blank=True, verbose_name='Полное описание')
    seo_title = models.TextField(
        blank=True, verbose_name='SEO title')
    seo_key = models.TextField(blank=True, verbose_name='SEO keys')
    seo_desc = models.TextField(
        blank=True, verbose_name='SEO content')
    full_url = models.TextField(
        blank=True, verbose_name='Полный URL')

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
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    country = models.CharField(max_length=100, verbose_name='страна')
    region = models.CharField(max_length=100, verbose_name='регион')
    # city = models.CharField(max_length=100, verbose_name='город')
    address = models.CharField(max_length=250, verbose_name='адрес')
    postal_code = models.CharField(max_length=20, verbose_name='индекс')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    email = models.EmailField()
    notes = models.TextField(max_length=500, blank=True,
                             verbose_name='примечание к заказу')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='оплачен')
    status = models.CharField(max_length=20,
                                    verbose_name='Статус заказа',
                                    choices=(
                                        ('new', 'Новый'),
                                        ('proc', 'На обработке'),
                                        ('arc', 'В архиве')), default='new')

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
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='цена')
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
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

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
