# Generated by Django 5.0.3 on 2024-04-06 08:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0008_remove_custorder_address_remove_custorder_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('customization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horofixapp.customizationdetail')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horofixapp.customwatch')),
                ('shopping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horofixapp.shoppingcart')),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='items',
            field=models.ManyToManyField(through='horofixapp.ShoppingCartItem', to='horofixapp.customwatch'),
        ),
    ]