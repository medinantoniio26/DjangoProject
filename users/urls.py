from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    #path('profile/', view_profile, name='profile'),
]