# Generated by Django 3.1.3 on 2021-10-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20211005_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='current_price',
            field=models.IntegerField(default=0),
        ),
    ]