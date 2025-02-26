from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    #path('login/', views.sign_in, name='login'),
    path('profile/', views.profile, name='profile'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_users/<int:user_id>/posts/', views.user_posts, name='user_posts'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('polls/', include('polls.urls')),  
   # path('post/edit/<int:id>/', user_views.edit_post, name='post-edit'), 
   # path('post/delete/<int:id>/', user_views.delete_post, name='post-delete'),

]



  