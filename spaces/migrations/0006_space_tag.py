# Generated by Django 5.1.1 on 2024-10-02 15:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0005_remove_space_picture_space_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='tag',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]