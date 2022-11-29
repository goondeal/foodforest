from django.core.management.base import BaseCommand
from restaurants.models import FoodCategory


class Command(BaseCommand):
    help = 'Adds food categories to the database'

    def handle(self, *args, **kwargs):
        fcs = [
            {
                'name': 'Fried Chicken',
                'name_ar': 'فرايد تشيكن',
            },
            {
                'name': 'Pizza',
                'name_ar': 'بيتزا',
            },
            {
                'name': 'Burger',
                'name_ar': 'برجر',
            },
            {
                'name': 'Grill',
                'name_ar': 'مشويات',
            },
        ]

        for fc in fcs:
            new_fc = FoodCategory(
                name=fc['name'],
                name_ar=fc['name_ar'],
                name_en=fc['name'],
            )
            new_fc.save()
