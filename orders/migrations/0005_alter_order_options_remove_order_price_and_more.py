# Generated by Django 4.1.3 on 2023-10-17 15:40

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_options_orderstatus_rank_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AddField(
            model_name='ordertype',
            name='description',
            field=models.CharField(default=' ', max_length=127),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordertype',
            name='description_ar',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AddField(
            model_name='ordertype',
            name='description_en',
            field=models.CharField(max_length=127, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user'], name='user_index'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['restaurant'], name='order_restaurant_index'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phone'], name='phone_index'),
        ),
    ]
