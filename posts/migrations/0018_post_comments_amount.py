# Generated by Django 4.2 on 2023-10-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_comment_dislikes_amount_post_dislikes_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_amount',
            field=models.IntegerField(default=0),
        ),
    ]
