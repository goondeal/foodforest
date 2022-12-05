from django.db import models
from restaurants.models import Restaurant, MenuItem
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class OrderType(models.Model):
    title = models.CharField(max_length=31)

    def __str__(self):
        return self.title


class OrderStatus(models.Model):
    title = models.CharField(max_length=63)
    color = models.CharField(max_length=31)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    type = models.ForeignKey(OrderType, related_name='type', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    phone = PhoneNumberField(null=True, blank=True, db_index=True)
    # If orderType is Delivery:
    captin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captin', on_delete=models.PROTECT, null=True, blank=True)
    

    prep_duration_sec = models.IntegerField(default=0, editable=False)
    delivery_duration_sec = models.IntegerField(default=0, editable=False)
    

class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    name = models.CharField(max_length=127)
    description = models.TextField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField()
    quantity = models.SmallIntegerField()

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    