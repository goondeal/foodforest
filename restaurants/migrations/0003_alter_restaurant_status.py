# Generated by Django 4.1.3 on 2022-12-01 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_alter_menuitem_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='restaurants.restaurantstatus'),
        ),
    ]
