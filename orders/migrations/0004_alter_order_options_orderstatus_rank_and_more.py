# Generated by Django 4.1.3 on 2022-12-13 17:46

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_delivery_duration_sec_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-delivered_at',)},
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='rank',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None),
        ),
    ]
