from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, CreateProductSerializer, ReviewSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        productsAll = Product.objects.all()
        serializer = ProductSerializer(productsAll, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductListApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

class ProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer


class CollectionListApiView(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_pk = self.request.query_params.get('product_pk')
        return Review.objects.get(product_pk=product_pk)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'POST':
            return CreateProductSerializer



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product(request, pk):
    product1 = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product1)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = CreateProductSerializer(product1, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        product1.delete()
        return Response(data={"message": f"Product with {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view()
def collections(request):
    collectionAll = Collection.objects.all()
    serializer = CollectionSerializer(collectionAll, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def collection(request, pk):
    collection1 = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection1)
    return Response(serializer.data, status=status.HTTP_200_OK)
