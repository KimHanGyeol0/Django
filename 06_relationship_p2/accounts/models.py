from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 내가 팔로잉하면 다른 사람한테는 팔로워, 대칭을 꺼야한다=>근데 이러면 역참조가 발생
    # => related_name 필요
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
