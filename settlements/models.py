from django.db import models
from restaurants.models import Restaurant
from django.conf import settings


class SettlementStatus(models.Model):
    title = models.CharField(max_length=31)

    def is_solved(self):
        return self.id == 1

    def __str__(self):
        return self.title


class Settlement(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE)
    status = models.ForeignKey(SettlementStatus, on_delete=models.PROTECT)
    note = models.TextField(max_length=511)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.restaurant.name + ' ' + self.user.get_full_name()