# Generated by Django 3.2.15 on 2022-10-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20221010_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcomment',
            name='likes_amount',
            field=models.IntegerField(default=0),
        ),
    ]
