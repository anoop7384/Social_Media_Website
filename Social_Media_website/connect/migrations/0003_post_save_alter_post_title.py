# Generated by Django 4.0.6 on 2022-08-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0002_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='save',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='0 Likes', max_length=100),
        ),
    ]
