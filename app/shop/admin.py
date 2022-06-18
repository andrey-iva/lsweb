from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage, Order, OrderItem, Post, Message
from .resources import ProductResource

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
    inlines = [ProductImageInline,]
    search_fields = ['name']
    fields = [
        'category', 'name', 'slug', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'attribute', 'image_base', 'preview', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc',
        'video_shot', 'preview_shot', 'video', 'preview_video',
    ]
    list_display = [
        'id', 'name', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'image_base', 'video', 'video_shot', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc',
    ]
    list_editable = [
        'name', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type', 'available', 'image_base', 'video', 'video_shot', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc',
    ]
    list_filter = ['category', 'available', 'brand_car']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['preview', 'preview_shot', 'preview_video']

    def preview(self, obj):
        return mark_safe(u'<img width=100 src="%s" />' % str(obj.image_base.url))

    def preview_shot(self, obj):
        return mark_safe(u'<img width="250" src="%s" />' % str(obj.video_shot.url))

    def preview_video(self, obj):
        return mark_safe(u'<video width="500" controls="controls"><source src="%s"></video>' % str(obj.video.url))
# end import - export

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'first_name', 'status', 'paid', 'grand_total', 'phone', 'created']
    list_filter = ['paid', 'status', 'created']
    exclude = ['yookassa_full_info', 'address_full_info']
    # list_editable = ['paid', 'status']
    inlines = [OrderItemInline]

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
