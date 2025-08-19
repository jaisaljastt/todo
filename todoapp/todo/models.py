# from django.db import models
# from django.contrib.auth.models import User

# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('todo', 'To Do'),
#         ('in-progress', 'In Progress'),
#         ('done', 'Done'),
#         ('failed', 'Failed'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')

#     def __str__(self):
#         return f"{self.text} ({self.get_status_display()})"

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),  # Changed from 'in-progress' to 'inprogress'
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.text} ({self.get_status_display()})"
