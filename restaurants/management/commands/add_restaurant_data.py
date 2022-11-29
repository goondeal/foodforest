import json
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, FoodCategory, MenuCategory, MenuItem, MenuItemFeatureCategory, MenuItemFeature


class Command(BaseCommand):
    help = 'Adds restaurant data to the db'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to <file>.json')

    def _is_english(self, text):
        return text.encode().isalpha()

    def handle(self, *args, **kwargs):
        fpath = kwargs['file_path']
        data = None
        with open(file=fpath, mode='r', encoding='utf-8') as f:
            data = json.loads(f.read())

        restaurant = Restaurant.objects.create(
            name=data["name"],
            slogan=data["slogan"],
            description=data["description"],
            address=data["address"],
            logo=data["logo"]
        )
        restaurant.category.add(FoodCategory.objects.get(name=data["category"]))
        restaurant.save()
        i = 1
        for menu_category in data["menu_categories"]:
            new_menu_category = MenuCategory.objects.create(
                title=menu_category["title"],
                restaurant=restaurant,
                ordering=i
            )
            for item in menu_category["items"]:
                new_item = MenuItem.objects.create(
                    name = item["name"],
                    description = item.get("description") or item.get("desc") or "",
                    price = item["price"],
                    menu_category = new_menu_category
                )
                for key in item.get("features", {}):
                    fcat = MenuItemFeatureCategory.objects.get(title=key) if self._is_english(key) else MenuItemFeatureCategory.objects.get(title_ar=key)
                    title = item["features"][key]
                    menu_item_feature = MenuItemFeature.objects.get(category=fcat, title=title) if self._is_english(title) else MenuItemFeature.objects.get(category=fcat, title_ar=title)
                    new_item.features.add(menu_item_feature)

            i += 1
