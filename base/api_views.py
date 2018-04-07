from base.serializers import CategoriesSerializer, SubCategoriesSerializer, ProductsSerializer, ProducersSerializer
from rest_framework import viewsets
from product.models import Product, Subcategory, Category, Producer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class SubCategoriesViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategoriesSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


class ProducersViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducersSerializer
