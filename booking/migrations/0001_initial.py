# Generated by Django 5.1.1 on 2024-12-06 09:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('space', '0009_alter_space_book_count_alter_space_schedule'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default='2003-08-04', null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('request_letter', models.FileField(blank=True, upload_to='request_letters/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='space.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('space', 'date', 'start_time', 'end_time')},
            },
        ),
    ]
