from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from connect.models import Post

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    isVerified = models.BooleanField(default=True, blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(default="Add your bio")
    savedPosts = models.ManyToManyField(
        Post, blank=True, related_name='user_saved_posts')
    likedPosts = models.ManyToManyField(
        Post, blank=True, related_name='user_liked_posts')
    followers = models.ManyToManyField(
        User, blank=True, related_name='following')
    following = models.ManyToManyField(
        User, blank=True, related_name='follower')
    follower_requests = models.ManyToManyField(
        User, blank=True, related_name='follower_request')
    following_requests = models.ManyToManyField(
        User, blank=True, related_name='following_request')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



