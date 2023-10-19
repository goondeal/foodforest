from django.db import models
from restaurants.models import Restaurant, MenuItem
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class OrderType(models.Model):
    '''
    Hall, takeaway, or delivery
    '''
    ORDER_TYPES_BASE_CHOICES = [
        ("H", "hall"),
        ("T", "takeaway"),
        ("D", "delivery")
    ]
    title = models.CharField(max_length=31)
    description = models.CharField(max_length=127)

    @property
    def is_delivery(self):
        return self.title == 'D'

    def __str__(self):
        return self.title


class OrderStatus(models.Model):
    '''
    sent -> seen -> being prepared -> on the way -> delivered
                  \
                   \
                    -> rejected
    '''
    title = models.CharField(max_length=63)
    color = models.CharField(max_length=31)
    rank = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user',
        on_delete=models.PROTECT
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)

    type = models.ForeignKey(
        OrderType,
        related_name='type',
        on_delete=models.PROTECT
    )
    # price = models.DecimalField(max_digits=9, decimal_places=2)
    note = models.TextField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField()
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.PROTECT,
        default=1
    )

    # If orderType is Delivery:
    captin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='captin',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    prepared_at = models.DateTimeField(editable=False, null=True)
    delivered_at = models.DateTimeField(editable=False, null=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['user'], name='user_index'),
            models.Index(fields=['restaurant'], name='order_restaurant_index'),
            models.Index(fields=['phone'], name='phone_index'),
        ]

    @property
    def price(self):
        items = self.items.all()
        subtotal = sum([item.price*item.quantity for item in items])
        # TODO: Edit after adding coupons app
        return subtotal

    # def save(self):
    #     if not self.pk:
    #         self.status
    #     return super().save(force_insert, force_update, using, update_fields)    

    def __str__(self):
        return f'{self.id} - {self.user.email} - {self.restaurant}'


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    name = models.CharField(max_length=127)
    description = models.TextField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    features = models.JSONField()
    quantity = models.PositiveSmallIntegerField()
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item.id} - {self.name}'
