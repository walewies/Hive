# Generated by Django 4.0.1 on 2022-04-09 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profiles/default_profile.jpeg', upload_to='profiles/'),
        ),
    ]
