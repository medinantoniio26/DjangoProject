import datetime
from django.contrib import admin
from blog.models import Post
from django.utils import timezone
from django.db import models
from django.apps import apps 

class Question(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    post = models.OneToOneField('blog.Post', on_delete=models.CASCADE, related_name='poll_post') 
    question_text = models.CharField(max_length=200, blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    def __str__(self):
        return self.title


    def get_posts(self):
        Post = apps.get_model('blog', 'Post') 
        return Post.objects.filter(poll=self)
