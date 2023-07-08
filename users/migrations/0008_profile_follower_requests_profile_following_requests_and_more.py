# Generated by Django 4.1.4 on 2023-06-28 18:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_profile_isverified_profile_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower_requests',
            field=models.ManyToManyField(blank=True, related_name='follower_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='following_requests',
            field=models.ManyToManyField(blank=True, related_name='following_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]