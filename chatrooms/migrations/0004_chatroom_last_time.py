# Generated by Django 4.1.4 on 2023-06-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0003_chatroom_last_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='last_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]