from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.utils import json

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


@csrf_exempt
def get_producer_by_id(request, pk):

    try:
        producer = Producer.objects.get(pk=pk)
    except Producer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProducersSerializer(producer)
        return JsonResponse(serializer.data)


@csrf_exempt
def get_product_by_id(request, pk):

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductsSerializer(product)
        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False), content_type="application/json")


@csrf_exempt
def get_category_by_id(request, pk):

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategoriesSerializer(category)
        return JsonResponse(serializer.data)


@csrf_exempt
def get_subcategory_by_id(request, pk):

    try:
        subcategory = Subcategory.objects.get(pk=pk)
    except Subcategory.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SubCategoriesSerializer(subcategory)
        return JsonResponse(serializer.data)
