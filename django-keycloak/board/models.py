from django.db import models
from django.contrib.auth.models import AbstractUser

# email이 기본키인 커스텀 유저 모델
class User(AbstractUser):
    email = models.EmailField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 게시글 객체
class Post(models.Model):
    title = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title