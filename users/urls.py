#from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/users/<int:user_id>/posts/', views.user_posts, name='user_posts'),
    
    #path('profile/', view_profile, name='profile'),
]
