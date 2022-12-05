from django.core.management.base import BaseCommand
from orders.models import OrderStatus


class Command(BaseCommand):
    help = 'Adds order statuses to the database'

    def handle(self, *args, **kwargs):
        statuses = [
            {
                'title': 'sent',
                'title_ar': 'تم الإرسال',
                'color': 'gray',
            },
            {
                'title': 'seen',
                'title_ar': 'تمت رؤيته',
                'color': 'yellow',
            },
            {
                'title': 'rejected',
                'title_ar': 'مرفوض',
                'color': 'yellow',
            },
            {
                'title': 'being prepared',
                'title_ar': 'يتم تحضيره',
                'color': 'yellow',
            },
            {
                'title': 'on the way',
                'title_ar': 'فى الطريق',
                'color': 'yellow',
            },
            {
                'title': 'delivered',
                'title_ar': 'تم توصيله',
                'color': 'red',
            },
        ]

        for s in statuses:
            new_status = OrderStatus(
                title=s['title'],
                title_ar=s['title_ar'],
                title_en=s['title'],
                color=s['color'],
            )
            new_status.save()
