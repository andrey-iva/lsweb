from django.urls import path, include

from .views import view, shop, cart, order, blog, cdek, error, pmap

app_name = 'shop'

handler404 = 'shop.views.error.page_not_found'
handler400 = 'shop.views.error.bad_request'
handler403 = 'shop.views.error.permission_denied'

urlpatterns = [
    path('', view.home, name='home'),
    path('make/map/', pmap.make_map, name='make_map'),
    path('about-us/', view.about, name='about'),
    path(u'доставка-и-оплата/', view.shipping_payment, name='shipping_payment'),
    path('pdd/', view.pdd, name='pdd'),
    path('video/', view.video_list, name='video_list'),
    path('policy/', view.policy, name='policy'),
    path('clear/session/', view.clear_session, name='clear_session'),
    path('contact/', include([
        path('', view.contact, name='contact'),
        path('form/', view.get_message_form, name='get_message_form'),
        path('<str:message>/', view.contact, name='contact'),
        path('send/massage/', view.contact_send_message, name='contact_send_message'),
    ])),
    path('shop/', shop.product_list, name='shop_page'),
    path('product/loop_id/', shop.loop_id, name='loop_id'),
    path('product/<slug:slug>/', shop.product_detail, name='product_detail'),
    # /product-category/{{brand}}/ - прописан жестко в product/list.html - 1 раз
    path(u'product-category/', include([
        path('аксессуары/', shop.product_list, name='product_list'),
        path('filter/', shop.product_filter, name='product_filter'),
        path('size/<int:size>/', shop.product_list_size, name='product_list_size'),
        path('sort/<str:sort_by>/', shop.product_sort_by, name='product_sort_by'),
        path('toggle/<str:view_style>/', shop.toggle_style, name='toggle_style'),
        path('<slug:category_slug>/', shop.product_list, name='product_list_by_category'),
        path('krepleniya-isofix/<slug:category_slug>/',
             shop.product_list, name='product_list_by_category'),
    ])),
    path('cart/', include([
        path('', cart.cart_detail, name='cart_detail'),
        path('remove/loop/marker/', cart.remove_loop_marker, name='remove_loop_marker'),
        path('json/', cart.cart_json, name='cart_json'),
        path('clear/', cart.cart_clear, name='cart_clear'),
        path('count/quantity/on/', cart.cart_count_quantity, name='cart_count_quantity'),
        path('add/<int:product_id>/', cart.cart_add, name='cart_add'),
        # /cart/remove/id - прописан жестко в JS
        path('remove/<int:product_id>/', cart.cart_remove, name='cart_remove'),
        # /cart/remove/loop/id - прописан жестко в JS
        path('remove/loop/<int:product_id>/', cart.cart_remove_loop, name='cart_remove_loop'),
        path('add/delivery/tax/', cart.add_delivery_tax, name='add_delivery_tax'),
        path('add/percent/', cart.add_percent, name='add_percent'),
        # del/sessionkeyloop/<int:product_id>/ - прописан жестко в JS
        path('del/sessionkeyloop/<int:product_id>/',
             cart.cart_loop_off, name='cart_loop_off'),
        path('set/marker/on/<int:product_id>/',
             cart.set_loop_marker_on, name='set_loop_marker_on'),
    ])),
    path('order/', include([
        path('create/', order.order_create, name='order_create'),
        path('created/', order.order_created, name='order_created'),
    ])),
    path('blog/', include([
        path('', blog.post_list, name='post_list'),
        path('<slug:post>/', blog.post_detail, name='post_detail'),
    ])),
    path('cdek/', include([
        path('tariffs/', cdek.tarifflist, name='tarifflist'),
        path('city/', cdek.get_city, name='get_city'),
        path('cities/', cdek.get_cities, name='get_cities'),
    ])),
    path('404/', error.page_not_found),
    path('400/', error.bad_request),
    path('403/', error.permission_denied),
    # re_path(r'^\w*', view.ret_index, name='ret_index'),
    # path('order/', include([])),
]
