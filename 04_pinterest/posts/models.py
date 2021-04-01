from django.db import models
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    content = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    # blank=True없으면 무조건 입력될 수 있게 만들어놔야함
    hashtags = models.ManyToManyField(Hashtag, related_name='posts', blank=True)


class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
