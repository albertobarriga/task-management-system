from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from apps.tasks.models import Task, Comment
from .serializers import UserSerializer, TaskSerializer, CommentSerializer

User = get_user_model()

# Authentication Endpoints
@api_view(['POST'])
@csrf_exempt
def register(request):
    """POST /api/auth/register/"""
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def login(request):
    """POST /api/auth/login/"""
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """POST /api/auth/logout/"""
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logged out successfully'})

@api_view(['POST'])
def refresh_token(request):
    """POST /api/auth/refresh/"""
    # Para simplificar, usamos sesiones de Django
    return Response({'message': 'Token refresh would be implemented with JWT'})

# User Management
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """GET /api/users/ (list with pagination)"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    """GET /api/users/{id}/ y PUT /api/users/{id}/"""
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """GET /api/users/me/"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Task Management
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):
    """GET /api/tasks/ y POST /api/tasks/"""
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, id):
    """GET/PUT/PATCH/DELETE /api/tasks/{id}/"""
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Task Operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_assign(request, id):
    """POST /api/tasks/{id}/assign/"""
    try:
        task = Task.objects.get(id=id)
        user_id = request.data.get('user_id')
        
        if user_id:
            user = User.objects.get(id=user_id)
            task.assigned_to.add(user)
            task.save()
            
            return Response({'message': f'Task assigned to {user.username}'})
        
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_comments(request, id):
    """GET /api/tasks/{id}/comments/ y POST /api/tasks/{id}/comments/"""
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)