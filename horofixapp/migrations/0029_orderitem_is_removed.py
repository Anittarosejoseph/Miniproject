# Generated by Django 4.2.7 on 2023-11-20 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0028_watchproduct_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
