import json
from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus, OrderType
from restaurants.serializers import RestaurantSerializer, MenuItemSerializer
from restaurants.models import MenuItem, Restaurant


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('title', 'color', 'rank',)


class OrderItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

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
        # read_only_fields = ('name', 'description', 'price')

    def validate(self, data):
        TRY_AGAIN_MSG = 'Refresh the page and review your order again befor checkout'
        menu_item = data.get('item')
        item_name = data.get('name', '')

        # Check that the item is_active
        if not menu_item.active:
            raise serializers.ValidationError(
                f'Menu item: {item_name} is not available now!')

        # Check that the other properties are as ordered by the user
        if item_name != menu_item.name:
            raise serializers.ValidationError(
                f'Menu item: {item_name} name has been changed. {TRY_AGAIN_MSG}')

        if data.get('description') != menu_item.description:
            raise serializers.ValidationError(
                f'Menu item: {item_name} description has been changed. {TRY_AGAIN_MSG}')

        if data.get('price') != menu_item.price:
            raise serializers.ValidationError(
                f'Menu item: {item_name} price has been changed. {TRY_AGAIN_MSG}')

        if data.get('features') != MenuItemSerializer(menu_item).data.get('features'):
            raise serializers.ValidationError(
                f'Menu item: {item_name} features has been changed. {TRY_AGAIN_MSG}')

        q = data.get('quantity')
        if not isinstance(q, int) or q <= 0:
            raise serializers.ValidationError(
                f'Menu item: {item_name} has unvalid quantity={q}')

        return data


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ('id', 'title', 'description')
        read_only_fields = ('description',)


class OrderSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=OrderType.objects.all())
    status = OrderStatusSerializer(required=False)
    # items = OrderItemSerializer(many=True)
    restaurant = serializers.SlugRelatedField(
        slug_field='slug', queryset=Restaurant.objects.all())

    class Meta:
        model = Order
        fields = (
            'id',
            # 'user',
            'restaurant',
            'type',
            'price',
            'note',
            # 'items',
            'status',
            'phone',
            'created_at',
            'prepared_at',
            'delivered_at',
        )
        read_only_fields = (
            'price',
            'status'
            'created_at',
            'prepared_at',
            'delivered_at'
        )

    def to_internal_value(self, data):
        result = super().to_internal_value(data)

        restaurant = result.get('restaurant')
        # Check that the restaurant is active and open at the moment.
        if not restaurant.active or not restaurant.status.is_open:
            raise serializers.ValidationError({
                'restaurant': f'Restaurant: {restaurant.name} is not recieving orders now!'
            })

        items = None
        try:
            items = [json.loads(item.replace("'", '"'))
                     for item in self.initial_data.getlist('items')]
        except:
            raise serializers.ValidationError({
                'order items': 'Please provide valid items in your order'
            })
        if not items:
            raise serializers.ValidationError({'order': 'Order is empty !!'})
        items_ids_set = set([item.get('item') for item in items])
        if not items_ids_set.issubset(restaurant.menu_items_ids):
            raise serializers.ValidationError({
                'order items': 'All order items must belong to the same restaurant'
            })
        result['items'] = items

        return result

    # TODO: Validate order price as well as items prices after integrating coupons app.
    # def validate(self, data):
    #     restaurant = data.get('restaurant')
    #     # Check that the restaurant is active and open now.
    #     if not restaurant.active or not restaurant.status.is_open:
    #         raise serializers.ValidationError(
    #             f'Restaurant: {restaurant.name} is not recieving orders now!')
    #     # check that all order items belong to the this restaurant
    #     # items = data.get('items')
    #     # print('self.initial_data.items =', self.initial_data.get('items'), '\n')
    #     # items = json.loads(item.replace("'", '"'))
    #     items = [json.loads(item.replace("'", '"')) for item in self.initial_data.getlist('items')]
    #     print('items =', items, '\n')

    #     if not items:
    #         raise serializers.ValidationError('Order is empty !!')
    #     items_ids_set = set([item.get('menu_item_id') for item in items])
    #     if not items_ids_set.issubset(restaurant.menu_items_ids):
    #         raise serializers.ValidationError(
    #             'All order items must belong to the same restaurant')

    #     return data

    def create(self, validated_data):
        # print('\nvalidated_data =', validated_data)
        items = validated_data.pop('items')
        # print('create items =', items)
        order_items_serializer = OrderItemSerializer(data=items, many=True)
        if order_items_serializer.is_valid(raise_exception=True):
            order = Order.objects.create(**validated_data)
            order_items_serializer.save(order=order)
        return order

    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        # Update order attributes
        instance.type = OrderType.objects.get(
            pk=validated_data.get('type', instance.type.id))
        instance.note = validated_data.get('note', instance.note)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        order_items_serializer = OrderItemSerializer(data=items, many=True)
        if order_items_serializer.is_valid(raise_exception=True):
            order_items_serializer.save(order=instance)

        return instance

    def to_representation(self, instance):
        # Base result
        result = super().to_representation(instance)
        # Include restaurant info
        restaurant = RestaurantSerializer(instance.restaurant).data
        result['restaurant'] = {
            'name': restaurant.get('name'),
            'slug': restaurant.get('slug'),
            'logo': restaurant.get('logo'),
            'status': restaurant.get('status')
        }
        # Include order type
        result['type'] = OrderTypeSerializer(instance.type).data
        # result['status'] = OrderStatusSerializer(instance.status).data
        result['items'] = OrderItemSerializer(instance.items, many=True).data

        # TODO: Include delivery captin info if order.type is delivery
        return result
