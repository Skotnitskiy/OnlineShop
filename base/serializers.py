from rest_framework import serializers

from product.models import Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')