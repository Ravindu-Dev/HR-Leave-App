from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, LeaveRequest, LeaveBalance

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Initialize leave balances for new employee
            if user.role == 'EMPLOYEE':
                LeaveBalance.objects.create(user=user, leave_type='SICK', balance_days=10)
                LeaveBalance.objects.create(user=user, leave_type='CASUAL', balance_days=12)
                LeaveBalance.objects.create(user=user, leave_type='ANNUAL', balance_days=15)
        return user

class LoginForm(AuthenticationForm):
    pass

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason', 'evidence']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'evidence': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        leave_type = cleaned_data.get('leave_type')
        evidence = cleaned_data.get('evidence')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before start date.")
            
            duration = (end_date - start_date).days + 1
            if leave_type == 'SICK' and duration > 2 and not evidence:
                raise forms.ValidationError("Medical evidence is required for sick leave exceeding 2 days.")
        
        return cleaned_data
