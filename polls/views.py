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
from blog.models import Post
from .forms import PollForm
from .models import Poll, Post

class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vote_count"] = self.object.choice_set.aggregate(Sum("votes")).get("votes__sum", 0)
        return context





class CreateQuestionView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/createnew.html"
    success_url = reverse_lazy("polls:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        context['post'] = get_object_or_404(Post, pk=post_id)
        return context

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        for i in range(1, 4):
            choice_text = self.request.POST.get(f'new_choice_{i}', '').strip()
            if choice_text:
                Choice.objects.create(
                    question=self.object,
                    choice_text=choice_text
                )
        return redirect(self.success_url)
    

def create_poll(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Verificar si el post ya tiene una encuesta asociada
    existing_poll = Poll.objects.filter(post=post).first()
    if existing_poll:
        return redirect('blog:post_detail', post_id=post.id)  # Redirige a los detalles del post

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.post = post  # Asociar la encuesta con el post
            poll.save()
            return redirect('blog:post_detail', post_id=post.id)  # Redirigir al post después de crear la encuesta
    else:
        form = PollForm()

    return render(request, 'polls/createnew.html', {'form': form, 'post': post})
    
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('blog:post_detail', args=[post.pk]))
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

class CreateQuestionWithoutPostView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/createnew.html"
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        self.object = form.save()

        for i in range(1, 4):
            choice_text = self.request.POST.get(f'new_choice_{i}', '').strip()
            if choice_text:
                Choice.objects.create(
                    question=self.object,
                    choice_text=choice_text
                )
        return redirect(self.success_url)

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
