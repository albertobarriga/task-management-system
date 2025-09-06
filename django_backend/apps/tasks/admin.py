from django.contrib import admin
from .models import Task, Tag, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'due_date', 'created_by', 'is_archived']
    list_filter = ['status', 'priority', 'is_archived']
    search_fields = ['title', 'description']
    filter_horizontal = ['assigned_to', 'tags']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'task__title']