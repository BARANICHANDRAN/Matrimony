from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

]