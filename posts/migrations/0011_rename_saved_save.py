# Generated by Django 3.2.15 on 2022-10-09 14:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0010_post_likes_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Saved',
            new_name='Save',
        ),
    ]
