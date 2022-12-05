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
    note = models.TextField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True, db_index=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    # If orderType is Delivery:
    captin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captin', on_delete=models.PROTECT, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    prepared_at = models.DateTimeField(editable=False)
    delivered_at = models.DateTimeField(editable=False)
    

class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    name = models.CharField(max_length=127)
    description = models.TextField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField()
    quantity = models.SmallIntegerField()

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    