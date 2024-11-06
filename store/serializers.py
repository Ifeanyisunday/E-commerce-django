from decimal import Decimal

from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView

from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    class Meta:
        model = Collection
        fields = ('id', 'title')


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # inventory = serializers.IntegerField()
    collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name='collection-detail'
    # )
    discount = serializers.SerializerMethodField(method_name='discount_price')

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'inventory', 'discount', 'collection')

    # collection = serializers.StringRelatedField()
    # discount = serializers.SerializerMethodField(method_name='discount_price')

    def discount_price(self, product: Product):
        return product.price * Decimal(0.10)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'description', 'inventory', 'collection')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product', 'title', 'content']
