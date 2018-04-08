from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from base.api_views import CategoriesViewSet, SubCategoriesViewSet, ProductsViewSet, ProducersViewSet, \
    get_producer_by_id, get_product_by_id, get_subcategory_by_id, get_category_by_id

router = routers.DefaultRouter()
router.register(r'api/categories', CategoriesViewSet)
router.register(r'api/subcategories', SubCategoriesViewSet)
router.register(r'api/products', ProductsViewSet)
router.register(r'api/producers', ProducersViewSet)

urlpatterns = [
    url(r'', include('product.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api/producer/(?P<pk>[0-9]+)/$', get_producer_by_id),
    url(r'^api/product/(?P<pk>[0-9]+)/$', get_product_by_id),
    url(r'^api/subcategory/(?P<pk>[0-9]+)/$', get_subcategory_by_id),
    url(r'^api/category/(?P<pk>[0-9]+)/$', get_category_by_id),
]
