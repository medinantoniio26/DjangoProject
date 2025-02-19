from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm



def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        is_admin = request.user.groups.filter(name='admins').exists()
        context = {'posts': posts, 'is_admin': is_admin}
        return render(request, 'blog/home.html', context)
    else:
        messages.error(request, "Debes iniciar sesión para ver este contenido.")
        return redirect('login')  



def create_post(request):
    is_admin = request.user.groups.filter(name='Admin').exists()  # Verificar si el usuario es administrador

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
        else:
            messages.error(request, 'Por favor, corrija los siguientes errores:')
            return render(request, 'blog/post_form.html', {'form': form, 'is_admin': is_admin})

@login_required
def edit_post(request, id):
    is_admin = request.user.groups.filter(name='Admin').exists()  # Verificar si el usuario es administrador
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': id, 'is_admin': is_admin}
        return render(request, 'blog/post_form.html', context)
    
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect('posts')
        else:
            messages.error(request, 'Por favor, corrija los siguientes errores:')
            return render(request, 'blog/post_form.html', {'form': form, 'is_admin': is_admin})

@login_required
def delete_post(request, id):
    is_admin = request.user.groups.filter(name='Admin').exists()  # Verificar si el usuario es administrador
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post, 'is_admin': is_admin}

    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html', context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicación eliminada.')
        return redirect('posts')

def about(request):
        return render(request, 'blog/about.html')