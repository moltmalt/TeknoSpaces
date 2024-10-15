# Generated by Django 5.1.1 on 2024-10-14 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0002_admin_first_name_admin_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space_title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=255)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('seating_capacity', models.PositiveIntegerField()),
                ('has_air_conditioner', models.BooleanField(default=False)),
                ('has_internet', models.BooleanField(default=False)),
                ('has_television', models.BooleanField(default=False)),
            ],
        ),
    ]
