# Generated by Django 4.1.3 on 2023-09-30 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_restaurant_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='is_available',
            new_name='active',
        ),
    ]
