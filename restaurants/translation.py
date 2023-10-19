from modeltranslation.translator import translator, TranslationOptions
from .models import FoodCategory, RestaurantStatus, MenuCategory, MenuItem, MenuItemFeatureCategory, MenuItemFeature


class RestaurantStatusTranslationOptions(TranslationOptions):
    fields = ('title',)


class FoodCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

class MenuCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

class MenuItemTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class MenuItemFeatureCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


class MenuItemFeatureTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(RestaurantStatus, RestaurantStatusTranslationOptions)
translator.register(FoodCategory, FoodCategoryTranslationOptions)
translator.register(MenuCategory, MenuCategoryTranslationOptions)
translator.register(MenuItem, MenuItemTranslationOptions)
translator.register(MenuItemFeatureCategory,
                    MenuItemFeatureCategoryTranslationOptions)
translator.register(MenuItemFeature, MenuItemFeatureTranslationOptions)
