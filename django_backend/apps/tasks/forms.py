from django import forms
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks with user assignment"""
    
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label="Assign to Users"
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 
                 'estimated_hours', 'actual_hours', 'assigned_users']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estimated_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0'}),
            'actual_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap-like classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        if self.instance and self.instance.pk:
            self.fields['assigned_users'].initial = self.instance.assigned_to.all()
    
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
            self.save_m2m()
            task.assigned_to.set(self.cleaned_data['assigned_users'])
        return task