from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from store.filter import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .models import Product, Collection, Review, Cart, CartItem, Order
from .pagination import DefaultPageNumberPagination
from .serializers import ProductSerializer, CollectionSerializer, CreateProductSerializer, ReviewSerializer, \
    CartSerializer, CartItemSerializer, AddToCartSerializer, CreateReviewSerializer, OrderSerializer, \
    OrderItemSerializer, CreateOrderSerializer, CreateCartSerializer
from .permissions import IsAdminOrReadOnly

# class ProductListApiView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
# class ProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
# class CollectionListApiView(ListCreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAuthenticated]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     collection_id = self.request.query_params.get('collection_id')
    #     name = self.request.query_params.get('name')
    #     queryset = Product.objects.filter(collection_id=collection_id)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializer
        elif self.request.method == 'POST':
            return CreateReviewSerializer
        return ReviewSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CreateCartSerializer
        return CreateCartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        if self.request.method == 'PATCH':
            return CartUpadteSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}

class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


