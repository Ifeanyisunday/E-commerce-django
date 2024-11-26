from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db import transaction
from store.models import Product, Collection, Review, Cart, CartItem, Order, OrderItem
from user.models import Customer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title')


class ProductSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()
    discount = serializers.SerializerMethodField(method_name='discount_price')

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'inventory', 'discount', 'collection')

    def discount_price(self, product: Product):
        return product.price * Decimal(0.10)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'description', 'inventory', 'collection')


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product', 'title', 'content']


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created_at']



class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']




class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class CartUpadteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product','unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'order_items']



class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']

            customer = get_object_or_404(Customer, id=user_id)
            cart_item = Cart.objects.filter(cart_id=cart_id)
            order = Order.objects.create(customer=customer)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price,
            )for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()

