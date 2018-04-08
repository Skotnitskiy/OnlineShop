from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

import api_views

router = routers.DefaultRouter()
router.register(r'api/categories', api_views.CategoriesViewSet)
router.register(r'api/subcategories', api_views.SubCategoriesViewSet)
router.register(r'api/products', api_views.ProductsViewSet)
router.register(r'api/producers', api_views.ProducersViewSet)

urlpatterns = [
    url(r'', include('product.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api/producer/(?P<pk>[0-9]+)/$', api_views.get_producer_by_id),
    url(r'^api/product/(?P<pk>[0-9]+)/$', api_views.get_product_by_id),
    url(r'^api/subcategory/(?P<pk>[0-9]+)/$', api_views.get_subcategory_by_id),
    url(r'^api/category/(?P<pk>[0-9]+)/$', api_views.get_category_by_id),
]
