from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    """View to display all tasks with optimized database queries"""
    tasks = Task.objects.select_related('created_by').all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    """View to display task details with optimized queries"""
    task = get_object_or_404(
        Task.objects.select_related('created_by'), 
        pk=pk
    )
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    """View to create a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    """View to update an existing task"""
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form})