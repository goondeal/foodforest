from django.core.management.base import BaseCommand
from restaurants.models import RestaurantStatus


class Command(BaseCommand):
    help = 'Adds restaurant status items to the database'

    def handle(self, *args, **kwargs):
        status = [
            {
                'title': 'open',
                'title_ar': 'مفتوح',
            },
            {
                'title': 'stand by',
                'title_ar': 'يستعد',
            },
            {
                'title': 'closed',
                'title_ar': 'مغلق'
            },
        ]

        for s in status:
            new_status = RestaurantStatus(
                title=s['title'],
                title_ar=s['title_ar'],
                title_en=s['title'],
            )
            new_status.save()
