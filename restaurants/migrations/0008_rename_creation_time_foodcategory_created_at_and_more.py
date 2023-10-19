# Generated by Django 4.1.3 on 2023-10-17 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0007_remove_menuitem_num_of_reviewers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodcategory',
            old_name='creation_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='menucategory',
            old_name='creation_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='menuitem',
            old_name='creation_time',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='menucategory',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owned_restaurants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RestaurantBlackList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='blocked_users',
            field=models.ManyToManyField(related_name='blocks', through='restaurants.RestaurantBlackList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='restaurantblacklist',
            constraint=models.UniqueConstraint(fields=('user', 'restaurant'), name='no_repeated_users_for_restaurant'),
        ),
    ]