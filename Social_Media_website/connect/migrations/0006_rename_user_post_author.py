# Generated by Django 4.1.4 on 2022-12-20 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0005_rename_author_post_user_remove_post_constent_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]
