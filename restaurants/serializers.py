from rest_framework import serializers
from .models import RestaurantStatus, Restaurant, MenuCategory, MenuItem, MenuItemFeature, MenuItemFeatureCategory
from management.models import City

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

    # def to_representation(self, instance):
    #     result = super().to_representation(instance)
    #     is_detailed = self.context.get('detailed')
    #     if is_detailed:
    #         result['items'] = MenuItemSerializer(
    #             instance.items, many=True).data
    #     return result


class RestaurantSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=RestaurantStatus.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    
    class Meta:
        model = Restaurant
        fields = ('slug', 'name', 'slogan', 'rating', 'city',
                  'num_of_reviewers', 'logo', 'address', 'status')
        read_only_fields = ('slug', 'rating', 'num_of_reviewers')

    # def validate_city(self, value):
    #     city = City.objects.filter()
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return super().validate(attrs)    
    
    def to_representation(self, instance):
        result = super().to_representation(instance)
        # TODO: Add status and city
        view = self.context.get('view')
        if view and view.action == 'retrieve':
            result['menu'] = MenuCategorySerializer(
                instance.menu, many=True).data
        return result
