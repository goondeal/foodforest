from django.core.management.base import BaseCommand
from orders.models import OrderType


class Command(BaseCommand):
    help = 'Adds order types to the database'

    def handle(self, *args, **kwargs):
        types = [
            {
                'title': 'hall',
                'title_ar': 'صالة',
            },
            {
                'title': 'take away',
                'title_ar': 'تيك اواى',
            },
            {
                'title': 'delivery',
                'title_ar': 'توصيل',
            },
        ]

        for t in types:
            new_type = OrderType(
                title=t['title'],
                title_ar=t['title_ar'],
                title_en=t['title'],
            )
            new_type.save()
