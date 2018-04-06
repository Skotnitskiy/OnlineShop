from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

import api_views

router = routers.DefaultRouter()
router.register(r'api/categories', api_views.CategoriesViewSet)

urlpatterns = [
    url(r'', include('product.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
