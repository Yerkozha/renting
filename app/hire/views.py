from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import status
from rest_framework import permissions

from .serializers import ProductSerializer, OrderedProductSerializer, OrderSerializer
from .models import OrderedProduct, ProductModel

from .handlers.hire_handler import HireHandler
from rest_framework import generics
from django.db.models import Count

class HireViewSet(
    generics.ListAPIView,
    generics.UpdateAPIView,
    generics.CreateAPIView,
    viewsets.GenericViewSet):

    queryset = ProductModel.objects.all()

    permission_classes = [permissions.AllowAny]
    SERIALIZER_CLASSES = {
        "create_product": ProductSerializer,
        "create_order": OrderSerializer
    }

    def get_serializer_class(self):
        if self.action == 'list':
                return OrderedProductSerializer
        elif self.action == 'update':
                return ProductSerializer
        return self.SERIALIZER_CLASSES.get(self.action)

    @action(methods=['POST'], detail=True)
    def create_order(self, request, pk=None):

        product = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_input = serializer.save()
        ordered_product = HireHandler().create_order(order_input, product)

        # transfer app mixin limit
        return Response(data=OrderedProductSerializer(ordered_product).data, status=status.HTTP_201_CREATED)



    @action(methods=['POST'], detail=False)
    def create_product(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_input = serializer.save()
        product = HireHandler().create_product(product_input)
        # transfer app mixin limit
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)