# Generated by Django 4.2.14 on 2024-08-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_cart_amount_discount_cart_coupon_discount_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
