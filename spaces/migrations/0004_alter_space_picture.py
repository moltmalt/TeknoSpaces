# Generated by Django 5.1.1 on 2024-10-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0003_space_delete_spaces'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
