# Generated by Django 2.2 on 2022-03-22 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20220322_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='totalPrice',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='totalPrice',
            field=models.FloatField(default=0),
        ),
    ]
