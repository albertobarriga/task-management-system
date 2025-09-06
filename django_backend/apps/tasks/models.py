from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TaskTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    default_status = models.CharField(max_length=20, default='pending')
    default_priority = models.CharField(max_length=20, default='medium')
    default_due_date_days = models.IntegerField(default=7)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Metod to create from template
    def create_task_from_template(self, created_by, due_date=None):
        from django.utils import timezone
        from datetime import timedelta
        
        task = Task.objects.create(
            title=self.name,
            description=self.description,
            status=self.default_status,
            priority=self.default_priority,
            due_date=due_date or (timezone.now() + timedelta(days=self.default_due_date_days)),
            estimated_hours=self.estimated_hours,
            created_by=created_by,
            template=self
        )
        task.tags.set(self.tags.all())
        return task

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtasks')

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    template = models.ForeignKey(
        TaskTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tasks_created_from_template'
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"

    class Meta:
        ordering = ['-created_at']

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['task', 'user']

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.task}"

    class Meta:
        ordering = ['-timestamp']
