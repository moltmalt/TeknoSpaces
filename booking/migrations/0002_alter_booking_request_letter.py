# Generated by Django 5.1.1 on 2024-12-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='request_letter',
            field=models.FileField(upload_to='request_letters/'),
        ),
    ]
