# Generated by Django 4.2 on 2023-10-04 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20221010_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='interests',
        ),
    ]
