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
            'img',
            'features',
            'rating',
            'num_of_reviews',
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
        fields = ('id', 'title', 'items')


class RestaurantSerializer(serializers.ModelSerializer):
    status = RestaurantStatusSerializer()

    class Meta:
        model = Restaurant
        fields = ('slug', 'name', 'slogan', 'rating',
                  'num_of_reviewers', 'logo', 'address', 'status')

    # def to_representation(self, instance):
    #     result = super().to_representation(instance)
    #     view = self.context.get('view')
    #     if view and view.action == 'retrieve':
    #         result['menu'] = MenuCategorySerializer(
    #             instance.menu, many=True).data
    #     return result


