from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
<<<<<<< HEAD
#from polls.models import Poll
from django.apps import apps
=======
from polls.models import Poll
from polls.models import Question
>>>>>>> 459100e (funcionaa)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='post_question')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poll = models.OneToOneField('polls.Poll', on_delete=models.SET_NULL, null=True, blank=True, related_name='post_poll')

    def __str__(self):
        return self.title
    
    def get_poll(self):
        Poll = apps.get_model('polls', 'Poll')
        return Poll.objects.get(post=self)

    class Meta:
        ordering = ['-published_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text