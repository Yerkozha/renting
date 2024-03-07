from collections import OrderedDict
from rest_framework import serializers
from .entity import ProductEntity, OrderEntity, OrderedProductEntity
from typing import Dict
from rest_framework.serializers import ListSerializer

from .models import ProductModel, OrderModel, OrderedProduct




class BaseSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return super().create(validated_data)

    def _create_base_entity(self, validated_data: Dict, entity_class=None):
        if not entity_class:
            return None
        dict_data = {}
        fields = self.fields
        for k, value in validated_data.items():
            if isinstance(fields[k], BaseSerializer) or isinstance(
                fields[k], ListSerializer
            ):
                if (
                    isinstance(fields[k], ListSerializer)
                    and getattr(fields[k].child, "create", None)
                ) or (
                    isinstance(fields[k], BaseSerializer)
                    and getattr(fields[k], "create", None)
                ):
                    serialized_value = (
                        None if value is None else fields[k].create(value)
                    )
                    dict_data[k] = serialized_value
                else:
                    dict_data[k] = value
            else:
                dict_data[k] = value
        return entity_class(**dict_data)


class ProductSerializer(BaseSerializer, serializers.ModelSerializer):

    def create(self, validated_data):
        return self._create_base_entity(validated_data, entity_class=ProductEntity)

    class Meta:
        model= ProductModel
        fields = '__all__'

class OrderSerializer(BaseSerializer, serializers.ModelSerializer):

    def create(self, validated_data):
        return self._create_base_entity(validated_data, entity_class=OrderEntity)

    class Meta:
        model= OrderModel
        fields = '__all__'


class OrderedProductSerializer(BaseSerializer, serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()

    def validate(self, data):



        return data

    def create(self, validated_data):

        return self._create_base_entity(validated_data, entity_class=OrderedProductEntity)

    class Meta:
        model= OrderedProduct
        fields = '__all__'






