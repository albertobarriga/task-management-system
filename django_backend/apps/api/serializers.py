from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.tasks.models import Task, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_usernames = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'due_date',
            'estimated_hours', 'actual_hours', 'created_by', 'created_by_username',
            'assigned_to', 'assigned_to_usernames', 'tags', 'parent_task',
            'metadata', 'created_at', 'updated_at', 'is_archived', 'template'
        ]
    
    def get_assigned_to_usernames(self, obj):
        return [user.username for user in obj.assigned_to.all()]

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'task', 'user', 'user_username', 'content', 'created_at']