# Generated by Django 4.0.1 on 2022-04-16 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.TextField(blank=True),
        ),
    ]
