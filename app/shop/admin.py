import logging
import uuid
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from urllib.parse import unquote
from pprint import pprint
from .models import Category, Product, ProductImage, Order, OrderItem, Post, Message
from .resources import ProductResource, ProductImageResource, PostResource


@admin.register(ProductImage)
class ProductImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'product', 'image']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'subject', 'email', 'notes']
    list_editable = ['status']
    list_filter = ['status']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(u'<img width=100 src="%s" />' % str(obj.image.url))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# import - export


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_per_page = 10
    search_help_text = 'Поиск по названию'
    resource_class = ProductResource
    inlines = [ProductImageInline, ]
    search_fields = ['name', 'item_number']
    fields = [
        'category', 'name', 'slug', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'attribute', 'image_base', 'preview', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc',
        'video_shot', 'preview_shot', 'video', 'preview_video', 'frame_video',
    ]
    list_display = [
        'id', 'name', 'item_number', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'image_base', 'video', 'video_shot', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc', 'frame_video',
    ]
    list_editable = [
        'name', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'image_base', 'video', 'video_shot', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc', 'frame_video'
    ]
    list_filter = ['category', 'available', 'brand_car', 'seat_type']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['preview', 'preview_shot', 'preview_video']
    actions = ['make_new_row']

    @admin.action(description='Создать похожий 1. Товары')
    def make_new_row(self, request, queryset):
        p = queryset[0]
        logging.debug('request: %s', request)
        logging.debug('queryset: %s', {
            'id': p.id,
            'category': p.category.id,
            'url': unquote(p.image_base.url).replace('/media', '') if p.image_base else ''
        })

        np = Product(
            category=p.category,
            name=p.name,
            slug=str(uuid.uuid1()),
            price=p.price,
            price_install=p.price_install,
            item_number=p.item_number,
            brand_car=p.brand_car,
            model_car=p.model_car,
            year=p.year,
            seat_type=p.seat_type,
            product_type=p.product_type,
            service_type=p.service_type,
            weight=p.weight,
            available=p.available,
            image_base=unquote(p.image_base.url).replace('/media', '') if p.image_base else '',
            description_short=p.description_short,
            description_full=p.description_full,
            seo_title=p.seo_title,
            seo_key=p.seo_key,
            seo_desc=p.seo_desc,
        )
        np.save()

        images = ProductImage.objects.filter(product_id=p.id)
        urls = []
        if images:
            for image in images:
                ProductImage(product_id=np.id, image=unquote(image.image.url).replace('/media', '')).save()
        
        return redirect(f'/admin/shop/product/{np.id}/change/')
        # queryset.update(status='p')

    def preview(self, obj):
        return mark_safe(u'<img width=250 src="%s" />' % str(obj.image_base.url))

    def preview_shot(self, obj):
        return mark_safe(u'<img width="250" src="%s" />' % str(obj.video_shot.url))

    def preview_video(self, obj):
        return mark_safe(u'<video width="500" preload="metadata" controls="controls"><source src="%s"></video>' % str(obj.video.url))

    class Media:
        js = ('/static/shop/assets/user.js',)
# end import - export


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'first_name', 'status', 'paid', 'grand_total', 'phone', 'created']
    list_filter = ['paid', 'status', 'created']
    exclude = ['yookassa_full_info']
    # list_editable = ['paid', 'status']
    inlines = [OrderItemInline]


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
