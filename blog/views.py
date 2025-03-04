from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm
from polls.models import Poll
from .models import Post

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated and (request.user.username == comment.author or request.user.groups.filter(name='admins').exists()):
        comment.delete()

def home(request):
    posts = Post.objects.all().select_related('poll') 
    is_admin = request.user.is_authenticated and request.user.groups.filter(name='admins').exists()
    
    context = {
        'posts': posts,
        'is_admin': is_admin,
    }
    
    return render(request, 'blog/home.html', context)

def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def create_post(request):
    post = None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Publicación creada exitosamente.')
            return redirect('polls:createnew', post_id=post.pk)
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def assign_poll_to_post(request, post_id, poll_id):
    post = get_object_or_404(Post, id=post_id)
    poll = get_object_or_404(Poll, id=poll_id)
    post.poll = poll
    post.save()
    messages.success(request, 'Encuesta asignada exitosamente.')
    return redirect('post-detail', pk=post.pk)
        

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    is_admin = request.user.groups.filter(name='admins').exists()

    if not (is_admin or post.author == request.user):
        messages.error(request, "No tienes permiso para editar esta publicación.")
        return redirect('home') 
        #return redirect('posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect('home') 
            #return redirect('posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'is_admin': is_admin})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    is_admin = request.user.groups.filter(name='admins').exists()

    if not (is_admin or post.author == request.user):
        messages.error(request, "No tienes permiso para eliminar esta publicación.")
        return redirect('home') 
        #return redirect('posts')

    if request.method == 'POST':
        if hasattr(post, 'poll_instance'):
            post.poll_instance.delete()
        post.delete()
        messages.success(request, 'Publicación eliminada.')
        return redirect('home') 
        #return redirect('posts')

    return render(request, 'blog/post_confirm_delete.html', {'post': post, 'is_admin': is_admin})

def about(request):
        return render(request, 'blog/about.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    is_admin = request.user.is_authenticated and request.user.groups.filter(name='admins').exists()
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'is_admin': is_admin})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username
            comment.created_at = timezone.now()  
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'form': form, 'post': post})
    

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated and (request.user.username == comment.author or request.user.groups.filter(name='admins').exists()):
        comment.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este comentario.")
    
    return redirect('post-detail', pk=comment.post.pk)
