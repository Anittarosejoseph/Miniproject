# Generated by Django 4.2.7 on 2024-03-06 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horofixapp', '0013_location_appoinment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomizedWatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WatchComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomizedWatchComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization_options', models.TextField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horofixapp.watchcomponent')),
                ('customized_watch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horofixapp.customizedwatch')),
            ],
        ),
        migrations.AddField(
            model_name='customizedwatch',
            name='components',
            field=models.ManyToManyField(through='horofixapp.CustomizedWatchComponent', to='horofixapp.watchcomponent'),
        ),
    ]
