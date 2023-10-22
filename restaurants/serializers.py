from rest_framework import serializers
from .models import *
from management.models import City


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'

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
        read_only_fields = (
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

class MenuItemAdminSerializer(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(
        queryset=MenuItemFeature.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = MenuItem
        # fields = '__all__'
        exclude = ['menu_category']
        # (
        #     'id',
        #     'name',
        #     'name_en',
        #     'name_ar',
        #     'description',
        #     'description_en',
        #     'description_ar',
        #     'price',
        #     'active',
        #     'img',
        #     'features',
        #     'rating',
        #     'num_of_reviews',
        # )
        read_only_fields = ('rating', 'num_of_reviews')
    
    # def validate(self, data):
    #     name = data.get('name', data.get('name_en', data.get('name_ar', '')))
    #     if not name:
    #         raise serializers.ValidationError("Please enter a valid item name")
    #     # description = data.get('description', data.get('description_en', data.get('description_ar', '')))
    #     # if not description:
    #     #     raise serializers.ValidationError("Please enter a valid item description")
    #     return super().validate(data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        features = MenuItemFeatureSerializer(instance.features, many=True).data
        response['features'] = {f['category']
                                ['title']: f['title'] for f in features}
        return response


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('id', 'title')
        read_only_fields = ('title', )

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['title'] = result.get('title') or instance.title_en or instance.title_ar
        result['items'] = MenuItemSerializer(
            instance.items.filter(active=True), many=True).data
        return result

class MenuCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('id', 'title', 'title_en', 'title_ar', 'active', 'ordering', 'created_at')

    # def validate(self, data):
    #     title = data.get('title', data.get('title_en', data.get('title_ar', '')))
    #     if not title:
    #         raise serializers.ValidationError("Please enter a valid title")

    #     return super().validate(data)    
        

class RestaurantSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(
        queryset=RestaurantStatus.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    categories = serializers.PrimaryKeyRelatedField(queryset=FoodCategory.objects.all(), many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ('slug', 'name', 'active', 'description', 'slogan', 'categories', 'rating', 'city',
                  'num_of_reviewers', 'logo', 'address', 'status')
        read_only_fields = ('slug', 'rating', 'num_of_reviewers')

    # def create(self, validated_data):
    #     categories = validated_data.pop('categories')
    #     istance = super().create(validated_data)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['status'] = RestaurantStatusSerializer(instance.status).data
        result['categories'] = FoodCategorySerializer(instance.categories, many=True).data
        # TODO: Add status and city
        view = self.context.get('view')
        if view and view.action == 'retrieve':
            result['menu'] = MenuCategorySerializer(
                instance.menu, many=True).data
        return result
