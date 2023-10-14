from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from management.models import City


class RestaurantStatus(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Restaurant statuses'

    def __str__(self):
        return f'{self.title} - {self.color}'

    @property
    def is_open(self):
        return self.title.lower() == 'open'


class FoodCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        blank=True,
        editable=False
    )
    img = models.ImageField(
        upload_to='categories-images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    ordering = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Food categories'
        ordering = ('ordering', 'name')

    @property
    def abs_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(FoodCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_restaurants',
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slogan = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(max_length=1023, blank=True, null=True)
    slug = models.SlugField(unique=True, allow_unicode=True, editable=False)

    rating = models.FloatField(editable=False, default=0.0)
    num_of_reviewers = models.PositiveIntegerField(editable=False, default=0)

    categories = models.ManyToManyField(FoodCategory)
    logo = models.ImageField(
        upload_to='restaurants-images/',
        blank=True,
        null=True
    )
    cover = models.ImageField(
        upload_to='restaurants-images/',
        blank=True,
        null=True
    )

    address = models.CharField(max_length=255)
    _longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    _latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    status = models.ForeignKey(
        RestaurantStatus, on_delete=models.PROTECT, null=True)

    blocked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='RestaurantBlackList')

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['owner'], name='owner_index'),
            models.Index(fields=['city'], name='city_index'),
        ]

    @property
    def location(self):
        if self._longitude and self._latitude:
            return f'{self._longitude},{self._latitude}'
        return ''

    @property
    def abs_url(self):
        return f'/restaurants/{self.slug}/'

    @property
    def menu(self):
        return self.menu_categories.all()

    @property
    def menu_items_ids(self):
        result = []
        for c in self.menu_categories.prefetch_related('items'):
            result += [item.id for item in c.items.all()]
        return result

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name, allow_unicode=True)
            if Restaurant.objects.filter(slug=slug).exists():
                slug = slugify(f'{self.name} {self.city.name}', allow_unicode=True)
                while Restaurant.objects.filter(slug=slug).exists():
                    random_num = str(datetime.now().timestamp()).split('.')[-1][-3:]
                    slug = slugify(f'{self.name} {self.city.name} {random_num}', allow_unicode=True)
            self.slug = slug
        super(Restaurant, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.name


class RestaurantBlackList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'], name='no_repeated_users_for_restaurant')
        ]


class MenuCategory(models.Model):
    title = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_categories',
    )
    ordering = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'Menu categories'
        ordering = ('ordering', 'id')
        indexes = [
            models.Index(fields=['restaurant'], name='restaurant_index')
        ]

    def __str__(self):
        return self.title

    @property
    def grouped_items(self):
        result = {}
        for item in self.items.all():
            if item.name in result:
                result[item.name].append(item)
            else:
                result[item.name] = [item]
        return result


class MenuItemFeatureCategory(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Menu-item feature categories'
        ordering = ('id',)

    def __str__(self):
        return self.title


class MenuItemFeature(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        MenuItemFeatureCategory,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.category} - {self.title}'


class MenuItem(models.Model):
    name = models.CharField(max_length=127)
    slug = models.SlugField(allow_unicode=True, editable=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    img = models.ImageField(
        upload_to='food-items-images/',
        blank=True,
        null=True
    )
    active = models.BooleanField(default=False)
    menu_category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    features = models.ManyToManyField(MenuItemFeature)

    rating = models.FloatField(editable=False, default=0.0)
    num_of_reviews = models.PositiveIntegerField(editable=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    ordering = models.SmallIntegerField(default=0)
    avg_prep_duration_sec = models.SmallIntegerField(default=0, editable=False)
    prep_time_nums = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ('ordering', 'id')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
