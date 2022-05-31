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
    list_per_page = 20
    resource_class = ProductResource
    inlines = [ProductImageInline,]
    fields = [
        'category', 'name', 'slug', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type',
        'available', 'image_base', 'preview', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc', 'full_url',
    ]
    list_display = [
        'id', 'category', 'name', 'slug', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type',
        'available', 'image_base', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc', 'full_url',
        # 'created', 'updated',
    ]
    list_filter = ['category', 'service_type', 'available', 'brand_car']
    list_editable = [
        'category', 'name', 'slug', 'price', 'price_install',
        'item_number', 'brand_car', 'model_car', 'year', 'seat_type', 'product_type',
        'service_type',
        'available', 'image_base', 'description_short',
        'description_full', 'seo_title', 'seo_key', 'seo_desc', 'full_url'
    ]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(u'<img width=400 src="%s" />' % str(obj.image_base.url))
# end import - export

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'status', 'paid', 'country', 'phone', 'email']
    list_filter = ['paid', 'status', 'created', 'updated']
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
