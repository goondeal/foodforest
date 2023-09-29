from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=128)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ordering = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('ordering', 'name',)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=128)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    ordering = models.SmallIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ('ordering', 'name',)

    def __str__(self):
        return self.name
