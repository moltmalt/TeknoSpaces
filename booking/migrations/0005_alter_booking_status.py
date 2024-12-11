# Generated by Django 5.1.1 on 2024-12-10 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved'), ('archived', 'Archived')], default='pending', max_length=10),
        ),
    ]
