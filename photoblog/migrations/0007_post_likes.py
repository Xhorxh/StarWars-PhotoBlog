# Generated by Django 3.2.18 on 2023-03-17 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoblog', '0006_remove_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]