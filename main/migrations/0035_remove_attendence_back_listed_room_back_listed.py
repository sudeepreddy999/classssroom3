# Generated by Django 4.2.5 on 2023-11-04 06:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_remove_room_back_listed_attendence_back_listed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendence',
            name='back_listed',
        ),
        migrations.AddField(
            model_name='room',
            name='back_listed',
            field=models.ManyToManyField(related_name='roomsStuBack', to=settings.AUTH_USER_MODEL),
        ),
    ]
