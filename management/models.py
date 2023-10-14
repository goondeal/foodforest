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
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'name'], name='no_repeated_states_for_a_country')
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
        constraints = [
            models.UniqueConstraint(
                fields=['state', 'name'], name='no_repeated_cities_for_a_state')
        ]

    def __str__(self):
        return self.name
