# Generated by Django 4.1.7 on 2023-03-10 19:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_alter_room_options_room_particpants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterField(
            model_name='room',
            name='particpants',
            field=models.ManyToManyField(blank=True, related_name='particpants', to=settings.AUTH_USER_MODEL),
        ),
    ]
