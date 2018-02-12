from django.conf.urls import url

from product.views import index, subcategory_product, product_details, cart, delete_from_cart, add_to_cart


app_name = 'product'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+)/$', subcategory_product,
        name='subcategory-product'),
    url(r'^(?P<id>\d+)/details/$', product_details,
        name='product-details'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^cart/delete/', delete_from_cart, name='delete-from-cart'),
    url(r'^cart/add/', add_to_cart, name='add-to-cart'),
]
