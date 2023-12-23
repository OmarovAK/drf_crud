from django.contrib import admin

from logistic.models import Product, StockProduct, Stock


class InlineStockProduct(admin.TabularInline):
    model = StockProduct
    extra = 0


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'title']
    ordering = ['id']


@admin.register(Stock)
class AdminStock(admin.ModelAdmin):
    inlines = [InlineStockProduct, ]
    list_display = ['id', 'address']
