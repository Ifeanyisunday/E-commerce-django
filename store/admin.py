from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product, Collection


# Register your models here.

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'price', 'description', 'inventory_status', 'collection')
    list_per_page = 10
    list_editable = ['price', 'description']
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product: Product):
        if product.inventory < 20:
            return 'Low'
        return 'Ok'


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'product_count')
    list_per_page = 10

    @admin.display(ordering='product')
    def product_count(self, collection: Collection):
        return collection.product_set.count()


