from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm



def home(request):
    posts = Post.objects.all()  
    is_admin = request.user.is_authenticated and request.user.groups.filter(name='admins').exists()
    context = {'posts': posts, 'is_admin': is_admin}
    return render(request, 'blog/home.html', context) 


@login_required
def create_post(request):
    is_admin = request.user.groups.filter(name='admins').exists()  

    if request.method == 'GET':
        context = {'form': PostForm(), 'is_admin': is_admin}
        return render(request, 'blog/post_form.html', context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Publicación creada exitosamente.')
            return redirect('posts')
        

from django.contrib.auth.models import Group

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    is_admin = request.user.groups.filter(name='admins').exists()

    if not (is_admin or post.author == request.user):
        messages.error(request, "No tienes permiso para editar esta publicación.")
        return redirect('posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect('posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'is_admin': is_admin})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    is_admin = request.user.groups.filter(name='admins').exists()

    if not (is_admin or post.author == request.user):
        messages.error(request, "No tienes permiso para eliminar esta publicación.")
        return redirect('posts')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicación eliminada.')
        return redirect('posts')

    return render(request, 'blog/post_confirm_delete.html', {'post': post, 'is_admin': is_admin})


def about(request):
        return render(request, 'blog/about.html')