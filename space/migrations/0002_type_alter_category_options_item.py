# Generated by Django 5.1.1 on 2024-10-14 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('third_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('fourth_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('fifth_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('sixth_image', models.ImageField(blank=True, null=True, upload_to='space_images')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('venue', models.CharField(max_length=100)),
                ('schedule', models.CharField(max_length=16)),
                ('seating_capacity', models.IntegerField()),
                ('hasAirConditioner', models.BooleanField()),
                ('hasInternet', models.BooleanField()),
                ('hasTelevision', models.BooleanField()),
                ('booked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='space', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space', to='space.category')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space', to='space.type')),
            ],
        ),
    ]
