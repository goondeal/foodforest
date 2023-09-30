from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2, primary_key=True)
    currency = models.CharField(max_length=31)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=128)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ordering = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('ordering', 'name',)
        indexes = [
            models.Index(fields=['country'], name='country_index')
        ]

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=128)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    ordering = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ('ordering', 'name',)
        indexes = [
            models.Index(fields=['state'], name='state_index')
        ]

    def __str__(self):
        return self.name
