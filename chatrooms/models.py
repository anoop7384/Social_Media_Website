from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatRoom(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_chatrooms')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver_chatrooms')
    last_text = models.TextField(default="")
    last_time = models.DateTimeField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username} - {self.timestamp}"
