from rest_framework import serializers

from product.models import Category, Subcategory, Product, Producer


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('__all__')


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class ProducersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('__all__')