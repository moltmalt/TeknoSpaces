# Generated by Django 5.1.1 on 2024-12-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0008_space_managed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='book_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='space',
            name='schedule',
            field=models.CharField(blank=True, default='abcdefghijklmnop', max_length=16, null=True),
        ),
    ]
