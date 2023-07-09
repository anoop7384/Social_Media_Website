from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# from cryptography.fernet import Fernet



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

    def encrypt_message(self, message):
        key = settings.ENCRYPTION_KEY  # Replace with your own encryption key
        cipher_suite = Fernet(key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        self.content = encrypted_message.decode()

    def decrypt_message(self):
        key = settings.ENCRYPTION_KEY  # Replace with your own encryption key
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(
            self.content.encode())
        return decrypted_message.decode()
