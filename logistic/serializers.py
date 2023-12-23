from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class SerializerStock(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['address', 'id']


class SerializerProduct(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'stocks']


class SerializerStockProduct(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['stock', 'product', 'quantity', 'price', ]
