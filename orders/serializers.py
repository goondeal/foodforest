from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus, OrderType


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('title', 'color',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'item',
            'name',
            'description',
            'price',
            'features',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'restaurant',
            'type',
            'status',
            'items',
            'price',
            'note',
            'created_at',
            'prepared_at',
            'delivered_at',
            'captin',
        )
