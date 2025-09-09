from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task
def send_task_notification(task_id, notification_type):
    """
    Send notifications for task events
    This is a mock implementation - in production would send emails/slack messages
    """
    try:
        task = Task.objects.get(id=task_id)
        print(f"📧 Notification: Task '{task.title}' - {notification_type}")
        print(f"   Assigned to: {[user.username for user in task.assigned_to.all()]}")
        
        # Simulate notification logic
        if notification_type == 'created':
            message = f"New task assigned: {task.title}"
        elif notification_type == 'updated':
            message = f"Task updated: {task.title}"
        elif notification_type == 'overdue':
            message = f"🚨 Task overdue: {task.title}"
        else:
            message = f"Task notification: {task.title}"
            
        print(f"   Message: {message}")
        
    except Task.DoesNotExist:
        print(f"Task {task_id} not found for notification")

@shared_task
def check_overdue_tasks():
    """
    Check for overdue tasks and mark them as overdue
    This runs periodically via Celery Beat
    """
    print("⏰ Checking for overdue tasks...")
    
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    )
    
    for task in overdue_tasks:
        old_status = task.status
        task.status = 'overdue'
        task.save()
        
        print(f"   Marked task '{task.title}' as overdue (was {old_status})")
        
        # Send notification
        send_task_notification.delay(task.id, 'overdue')
    
    print(f"   Found {len(overdue_tasks)} overdue tasks")

@shared_task
def cleanup_archived_tasks():
    """
    Cleanup archived tasks older than 30 days
    """
    print("🧹 Cleaning up archived tasks...")
    
    from datetime import timedelta
    cutoff_date = timezone.now() - timedelta(days=30)
    
    old_archived_tasks = Task.objects.filter(
        is_archived=True,
        updated_at__lt=cutoff_date
    )
    
    count = old_archived_tasks.count()
    old_archived_tasks.delete()
    
    print(f"   Deleted {count} old archived tasks")