# Generated by Django 5.0.3 on 2024-04-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0017_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customization',
            field=models.ManyToManyField(through='horofixapp.CartItem', to='horofixapp.customizationdetail'),
        ),
    ]