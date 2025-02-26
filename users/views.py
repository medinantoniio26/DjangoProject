from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from blog.models import Post  
from .forms import PostForm

def sign_in(request):

    if request.method == 'GET':
        
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hola {username.title()}, Bienvendo de nuevo!')
                return redirect('posts')
        
        messages.error(request,f'Usuario o Contraseña incorrectos.')
        return render(request,'users/login.html',{'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'Se cerró la Sesión.')
    return redirect('login')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Accedió Correctamente.')
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = User.objects.all()
    return render(request, 'users/admin_users.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_users')

@user_passes_test(lambda u: u.is_superuser)
def user_posts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user)
    is_admin = request.user.is_authenticated and request.user.is_superuser
    return render(request, 'users/user_posts.html', {'user': user, 'posts': posts, 'is_admin': is_admin})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    is_admin = request.user.is_authenticated and request.user.is_superuser
    return render(request, 'blog/my_posts.html', {'posts': posts, 'is_admin': is_admin})


 
"""
@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect('posts')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})"""