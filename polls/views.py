from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Choice, Question
from .forms import QuestionForm
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View


class IndexView(ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
"""
def index(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        new_question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now()
        )
    
        for i in range(1, 4):  
            choice_text = request.POST.get(f'new_choice_{i}')
            if choice_text:
                Choice.objects.create(
                    question=new_question,
                    choice_text=choice_text
                )

        return redirect('polls:index') 
    """  """
    latest_question_list = Question.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list
    })
    """

class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""

class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vote_count"] = self.object.choice_set.aggregate(Sum("votes")).get("votes__sum", 0)
        """
        try:
            vote_count = self.object.choice_set.aggregate(Sum('votes'))['votes__sum']
            context['vote_count'] = vote_count
        except KeyError:
            context['vote_count'] = 0
        """
        return context


class CreateQuestionView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/createnew.html"
    #success_url = '/'
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        self.object = form.save()

        #new_choice_text = self.request.POST.get('new_choice', '').strip()
        for i in range(1, 4):
            choice_text = self.request.POST.get(f'new_choice_{i}', '').strip()
            if choice_text:
                Choice.objects.create(
                    question=self.object,
                    choice_text=choice_text
                )
        
        return redirect('polls:createnew')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_question_list'] = Question.objects.all().order_by('-pub_date')
        return context

class VoteView(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "No seleccionaste una respuesta, intenta de nuevo.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return redirect('polls:results', pk=question.id)


class ResetVotesView(View):
    def post(self, request, question_id):
    #if request.method == 'POST': 
       # try:
            question = get_object_or_404(Question, pk=question_id)
            question.choice_set.update(votes=0)
            return redirect('polls:results', pk=question.id)
        #except Question.DoesNotExist:
            #return redirect('polls:index')
    #else:
        #return redirect('polls:index')
    def get(self, request, question_id):
        return redirect('polls:index')

class EditQuestionView(UpdateView):
    model = Question
    fields = ["question_text"]
    template_name = "polls/edit.html"
    success_url = reverse_lazy("polls:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choices"] = Choice.objects.filter(question=self.object)
        return context

    """   
    def edit(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        
        if request.method == "POST":
            question.question_text = request.POST.get('question_text')
            question.save()

            return redirect('polls:index')

        choices = Choice.objects.filter(question=question)
        
        context = {
            'question': question,
        }
        
        return render(request, 'polls/edit.html', context)
    """

    """
    def delete_question(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return redirect("polls:index")
    """

class DeleteQuestionView(DeleteView):
    model = Question
    template_name = "polls/confirm_delete.html"
    success_url = reverse_lazy("polls:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_question_list'] = Question.objects.all().order_by('-pub_date')
        return context
