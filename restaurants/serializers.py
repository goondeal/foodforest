from rest_framework import serializers
from .models import RestaurantStatus, Restaurant, MenuCategory, MenuItem, MenuItemFeature, MenuItemFeatureCategory


class RestaurantStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantStatus
        fields = ('title', 'color', 'is_open')



class MenuItemFeatureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemFeatureCategory
        fields = ('title',)


class MenuItemFeatureSerializer(serializers.ModelSerializer):
    category = MenuItemFeatureCategorySerializer()

    class Meta:
        model = MenuItemFeature
        fields = ('title', 'category')


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            'id',
            'name',
            'description',
            'price',
            'img_url',
            'features',
            'rating',
            'num_of_reviewers',
            'available_now',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        features = MenuItemFeatureSerializer(instance.features, many=True).data
        response['features'] = {f['category']
                                ['title']: f['title'] for f in features}
        return response



class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    class Meta:
        model = MenuCategory
        fields = ('title', 'items')



class RestaurantShallowSerializer(serializers.ModelSerializer):
    status = RestaurantStatusSerializer()

    class Meta:
        model = Restaurant
        fields = ('slug', 'name', 'slogan', 'rating',
                  'num_of_reviewers', 'logo', 'address', 'status')


class RestaurantFullSerializer(serializers.ModelSerializer):
    status = RestaurantStatusSerializer()
    class Meta:
        model = Restaurant
        fields = '__all__'

