from django.db import models
from django.contrib.auth.models import AbstractUser

# HARDCODED: Three types of leave available in the system
# SICK - For medical/health-related absences
# CASUAL - For short-term personal needs
# ANNUAL - For vacation/planned time off
LEAVE_TYPE_CHOICES = (
    ('SICK', 'Sick Leave'),
    ('CASUAL', 'Casual Leave'),
    ('ANNUAL', 'Annual Leave'),
)

class User(AbstractUser):
    # HARDCODED: Two user roles in the system - employees can request leave, managers can approve/reject
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')  # HARDCODED: Default role is EMPLOYEE
    department = models.CharField(max_length=100, blank=True, null=True)  # HARDCODED: Max 100 characters for department name
    job_title = models.CharField(max_length=100, blank=True, null=True)  # HARDCODED: Max 100 characters for job title

    def is_manager(self):
        return self.role == 'MANAGER'  # HARDCODED: Check if user role is MANAGER

class LeaveBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    balance_days = models.FloatField(default=0.0)  # HARDCODED: Default balance is 0.0 days (set during user creation)

    class Meta:
        unique_together = ('user', 'leave_type')

    def __str__(self):
        return f"{self.user.username} - {self.leave_type}: {self.balance_days}"

class LeaveRequest(models.Model):
    # HARDCODED: Three status states for leave request workflow
    # PENDING - Awaiting manager review
    # APPROVED - Manager approved, balance deducted
    # REJECTED - Manager rejected the request
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests') # HARDCODED: Foreign key to User model
    start_date = models.DateField() # HARDCODED: Start date of leave request
    end_date = models.DateField() # HARDCODED: End date of leave request
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES) # HARDCODED: Type of leave (SICK, CASUAL, ANNUAL)
    reason = models.TextField() # HARDCODED: Reason for leave request
    evidence = models.FileField(upload_to='evidence/', null=True, blank=True)  # HARDCODED: Upload path for evidence files
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')  # HARDCODED: New requests start as PENDING
    manager_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # HARDCODED: Timestamp of request creation

    def duration_days(self):
        return (self.end_date - self.start_date).days + 1  # HARDCODED: +1 to make date range inclusive (both start and end dates count)
    
    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"
