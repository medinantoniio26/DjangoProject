from django import forms
from .models import Question, Choice
from .models import Poll
from blog.models import Post

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']  