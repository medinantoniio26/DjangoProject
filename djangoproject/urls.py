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
    #path('accounts/', include('django.contrib.auth.urls')),
]
