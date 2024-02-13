# Generated by Django 4.2.7 on 2024-02-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0003_alter_customuser_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchproduct',
            old_name='watch_model',
            new_name='watch_modelnumber',
        ),
        migrations.AddField(
            model_name='watchproduct',
            name='warranty',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='watchproduct',
            name='category',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Kids', 'Kids')], default=None, max_length=10),
        ),
    ]
