# Generated by Django 5.1.1 on 2024-12-06 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_customuser_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
