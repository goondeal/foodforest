# Generated by Django 4.1.3 on 2022-12-05 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_time',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='orderstatus',
            name='color',
            field=models.CharField(default=11, max_length=31),
            preserve_default=False,
        ),
    ]
