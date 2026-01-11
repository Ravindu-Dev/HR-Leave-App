from django.db import models
from django.contrib.auth.models import AbstractUser

LEAVE_TYPE_CHOICES = (
    ('SICK', 'Sick Leave'),
    ('CASUAL', 'Casual Leave'),
    ('ANNUAL', 'Annual Leave'),
)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    department = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    def is_manager(self):
        return self.role == 'MANAGER'

class LeaveBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    balance_days = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'leave_type')

    def __str__(self):
        return f"{self.user.username} - {self.leave_type}: {self.balance_days}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()
    evidence = models.FileField(upload_to='evidence/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    manager_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"
