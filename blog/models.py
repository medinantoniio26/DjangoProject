from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from polls.models import Question  # Importa el modelo Question

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con la encuesta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)