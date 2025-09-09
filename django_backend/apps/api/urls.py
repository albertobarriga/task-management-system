from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication Endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/refresh/', views.refresh_token, name='refresh'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('users/me/', views.current_user, name='current_user'),
    
    # Task Management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    
    # Task Operations
    path('tasks/<int:id>/assign/', views.task_assign, name='task_assign'),
    path('tasks/<int:id>/comments/', views.task_comments, name='task_comments'),
]