from base.serializers import CategoriesSerializer
from rest_framework import viewsets
from product.models import Product, Subcategory, Order, OrderDetails, Category


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
