# Generated by Django 4.2.7 on 2023-12-02 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0004_remove_customuser_pincode_customuser_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
