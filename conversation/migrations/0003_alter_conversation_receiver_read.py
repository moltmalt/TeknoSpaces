# Generated by Django 5.1.1 on 2024-12-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0002_remove_conversation_is_read_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='receiver_read',
            field=models.BooleanField(default=False),
        ),
    ]
