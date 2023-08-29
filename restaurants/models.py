from django.db import models
from django.utils.text import slugify


class RestaurantStatus(models.Model):
    title = models.CharField(max_length=63)
    color = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Restaurant statuses'

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        return self.id == 1


class FoodCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, allow_unicode=True, blank=True, editable=False)
    img = models.ImageField(
        upload_to='food-categories-images/', blank=True, null=True,)
    creation_time = models.DateTimeField(editable=False, auto_now_add=True)
    ordering = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Food categories'
        ordering = ('ordering', 'name',)

    @property
    def abs_url(self):
        return f'/{self.slug}/'

    @property
    def img_url(self):
        return self.img.url if self.img else ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(FoodCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=63)
    slogan = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(max_length=1023, blank=True, null=True)
    slug = models.SlugField(unique=True, allow_unicode=True, editable=False)

    rating = models.FloatField(editable=False, default=0.0)
    num_of_reviewers = models.IntegerField(editable=False, default=0)

    category = models.ManyToManyField(FoodCategory)
    logo = models.ImageField(
        upload_to='restaurants-images/', blank=True, null=True)
    cover = models.ImageField(
        upload_to='restaurants-images/', blank=True, null=True)

    address = models.CharField(max_length=255)
    _long = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    _lat = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    status = models.ForeignKey(
        RestaurantStatus, on_delete=models.PROTECT, default=3)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def location(self):
        if self._long == None or self._lat == None:
            return ''
        return f'{self._long},{self._lat}'

    @property
    def abs_url(self):
        return f'/restaurants/{self.slug}/'

    @property
    def menu(self):
        return self.menu_categories.all()    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    title = models.CharField(max_length=63)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='menu_categories',
    )
    ordering = models.SmallIntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'Menu categories'
        ordering = ('ordering', 'id')

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
    title = models.CharField(max_length=63)

    class Meta:
        verbose_name_plural = 'Menu-item feature categories'
        ordering = ('id',)

    def __str__(self):
        return self.title


class MenuItemFeature(models.Model):
    title = models.CharField(max_length=63)
    category = models.ForeignKey(
        MenuItemFeatureCategory,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=127)
    slug = models.SlugField(allow_unicode=True, editable=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.ImageField(
        upload_to='food-items-images/', blank=True, null=True)

    menu_category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items',
    )
    features = models.ManyToManyField(MenuItemFeature)

    rating = models.FloatField(editable=False, default=0.0)
    num_of_reviewers = models.IntegerField(editable=False, default=0)

    available_now = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)

    ordering = models.SmallIntegerField(default=0)
    avg_prep_duration_sec = models.SmallIntegerField(default=0, editable=False)
    prep_time_nums = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ('ordering', 'id')

    @property
    def img_url(self):
        return self.img.url if self.img else ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
