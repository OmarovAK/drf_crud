from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView

from logistic.models import Product, Stock, StockProduct
from logistic.serializers import SerializerProduct, SerializerStock, SerializerStockProduct


class CreateProduct(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = SerializerProduct


class ListProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SerializerProduct
    filter_backends = [SearchFilter, ]
    search_fields = ['title', 'description', ]


class DeleteProduct(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = SerializerProduct


class AddStock(CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = SerializerStock


class ListStock(ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = SerializerStock


class AddStockProduct(CreateAPIView):
    queryset = StockProduct.objects.all()
    serializer_class = SerializerStockProduct


class StockDetail(RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = SerializerStock
