from django.contrib import admin
from .models import RestaurantStatus, FoodCategory, MenuCategory, MenuItemFeatureCategory, MenuItemFeature, MenuItem, Restaurant
from modeltranslation.admin import TranslationAdmin

class RestaurantStatusAdmin(TranslationAdmin):
    pass

class FoodCategoryAdmin(TranslationAdmin):
    pass

class MenuItemFeatureCategoryAdmin(TranslationAdmin):
    pass

class MenuItemFeatureAdmin(TranslationAdmin):
    pass

# Register your models here.
admin.site.register(RestaurantStatus, RestaurantStatusAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(MenuItemFeatureCategory, MenuItemFeatureCategoryAdmin)
admin.site.register(MenuItemFeature, MenuItemFeatureAdmin)
admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
