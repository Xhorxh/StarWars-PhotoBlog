# Generated by Django 3.2.18 on 2023-03-15 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoblog', '0003_rename_name_comment_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='username',
            new_name='name',
        ),
    ]
