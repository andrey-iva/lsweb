from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.template.defaultfilters import slugify

from .lbs import clean_string
from .models import Category, Product

class ForeignkeyRequiredWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            obj, created = self.model.objects.get_or_create(name = value.upper(), slug = slugify( clean_string(value) ))
            return obj
        else:
            raise ValueError(self.field+ " required")

class ProductResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='UUID')
    category = fields.Field(column_name='Категория', attribute='category', 
        widget=ForeignkeyRequiredWidget(Category, 'name'),
        saves_null_values=False)
    name = fields.Field(attribute='name', column_name='Название')
    slug = fields.Field(attribute='slug', column_name='Слаг')
    price = fields.Field(attribute='price', column_name='Цена товара')
    price_install = fields.Field(attribute='price_install', column_name='Цена установки')
    item_number = fields.Field(attribute='item_number', column_name='Артикул')
    brand_car = fields.Field(attribute='brand_car', column_name='Модель авто')
    model_car = fields.Field(attribute='model_car', column_name='Марка авто')
    year = fields.Field(attribute='year', column_name='Год выпуска')
    seat_type = fields.Field(attribute='seat_type', column_name='Тип сиденья')
    product_type = fields.Field(attribute='product_type', column_name='Тип продукта')
    service_type = fields.Field(attribute='service_type', column_name='Тип Услуги')
    available = fields.Field(attribute='available', column_name='Есть в наличии')
    image_base = fields.Field(attribute='image_base', column_name='Изображение')
    description_short = fields.Field(attribute='description_short', column_name='Короткое описание')
    description_full = fields.Field(attribute='description_full', column_name='Полное описание')
    seo_title = fields.Field(attribute='seo_title', column_name='SEO Заголовок')
    seo_key = fields.Field(attribute='seo_key', column_name='SEO Ключевые слова')
    seo_desc = fields.Field(attribute='seo_desc', column_name='SEO Описание')
    attribute = fields.Field(attribute='attribute', column_name='Атрибут')
    # full_url = fields.Field(attribute='full_url', column_name='Полный URL')
    # created = fields.Field(attribute='created', column_name='Был добавлен')
    # updated = fields.Field(attribute='updated', column_name='Был обновлен')

    def for_delete(self, row, instance):
        pass

    def clean(self, value, row=None, *args, **kwargs):
        print(value)

    class Meta:
        model = Product
        skip_unchanged = True
        exclude = ('full_url',)
        # report_skipped = False