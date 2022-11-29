from django.core.management.base import BaseCommand
from restaurants.models import MenuItemFeatureCategory, MenuItemFeature


class Command(BaseCommand):
    help = 'Add basic items features to the database'

    def handle(self, *args, **kwargs):
        feature_categories = [
            {
                "title_en": "size",
                "title_ar": "الحجم",
                "children": [
                    {
                        "title_en": "small",
                        "title_ar": "صغير",
                    },
                    {
                        "title_en": "medium",
                        "title_ar": "وسط",
                    },
                    {
                        "title_en": "large",
                        "title_ar": "كبير",
                    },
                    {
                        "title_en": "single",
                        "title_ar": "عادى",
                    },
                    {
                        "title_en": "double",
                        "title_ar": "مضاعف",
                    },
                ]
            },
            {
                "title_en": "taste",
                "title_ar": "الطعم",
                "children": [
                    {
                        "title_en": "regular",
                        "title_ar": "عادى",
                    },
                    {
                        "title_en": "spicy",
                        "title_ar": "حار",
                    }
                ]
            },
        ]

        for category in feature_categories:
            cat = MenuItemFeatureCategory.objects.create(
                title_en=category["title_en"],
                title_ar=category["title_ar"]
            )
            for feature in category["children"]:
                f = MenuItemFeature.objects.create(
                    title_en=feature["title_en"],
                    title_ar=feature["title_ar"],
                    category=cat
                )
