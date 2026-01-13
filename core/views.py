from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import RegisterForm, LoginForm, LeaveRequestForm
from .models import User, LeaveBalance, LeaveRequest

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_manager():
        return redirect('manager_dashboard')
    
    # Employee Dashboard
    balances = LeaveBalance.objects.filter(user=user)
    my_requests = LeaveRequest.objects.filter(user=user).order_by('-created_at')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = user
            
            # Check Balance Logic
            duration = leave_request.duration_days()
            balance_obj = balances.filter(leave_type=leave_request.leave_type).first()
            
            if balance_obj and balance_obj.balance_days >= duration:
                leave_request.save()
                messages.success(request, 'Leave application submitted successfully.')
                # TODO: Send Email to Manager
                return redirect('dashboard')
            else:
                messages.error(request, f'Insufficient balance for {leave_request.leave_type}. Required: {duration}, Available: {balance_obj.balance_days if balance_obj else 0}')
    else:
        form = LeaveRequestForm()

    return render(request, 'core/employee_dashboard.html', {
        'balances': balances,
        'requests': my_requests,
        'form': form,
    })

@login_required
def manager_dashboard_view(request):
    if not request.user.is_manager():
        return redirect('dashboard')
    
    # HARDCODED: Filter for PENDING status to show only requests awaiting manager action
    pending_requests = LeaveRequest.objects.filter(status='PENDING').order_by('created_at')
    
    return render(request, 'core/manager_dashboard.html', {
        'requests': pending_requests,
    })

@login_required
def approve_leave(request, leave_id):
    if not request.user.is_manager():
        return redirect('dashboard')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    if leave_request.status == 'PENDING':  # HARDCODED: Only PENDING requests can be approved
        # Deduct Balance
        balance = LeaveBalance.objects.filter(user=leave_request.user, leave_type=leave_request.leave_type).first()
        duration = leave_request.duration_days()
        
        if balance and balance.balance_days >= duration:
            balance.balance_days -= duration
            balance.save()
            
            leave_request.status = 'APPROVED'  # HARDCODED: Set status to APPROVED after successful approval
            leave_request.save()
            
            # TODO: Email PDF to User
            messages.success(request, f'Leave for {leave_request.user.username} approved.')
        else:
            messages.error(request, 'User has insufficient balance to approve this request.')
            
    return redirect('manager_dashboard')

@login_required
def reject_leave(request, leave_id):
    if not request.user.is_manager():
        return redirect('dashboard')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    if leave_request.status == 'PENDING':  # HARDCODED: Only PENDING requests can be rejected
        leave_request.status = 'REJECTED'  # HARDCODED: Set status to REJECTED
        leave_request.save()
        messages.info(request, f'Leave for {leave_request.user.username} rejected.')
        
    return redirect('manager_dashboard')

@login_required
def download_permission_letter(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    # Security: Only Manager or the Owner can download
    if not (request.user.is_manager() or request.user == leave_request.user):
        return redirect('dashboard')
    
    if leave_request.status != 'APPROVED':  # HARDCODED: Only APPROVED leaves can generate permission letters
        return HttpResponse("Letter only available for approved leaves.", status=403)  # HARDCODED: HTTP 403 Forbidden

    template_path = 'core/permission_letter_pdf.html'  # HARDCODED: Template path for PDF generation
    context = {'leave': leave_request}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="permission_letter_{leave_id}.pdf"'  # HARDCODED: PDF filename pattern
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def calendar_api(request):
    # Public team calendar or internal
    events = []
    approved_leaves = LeaveRequest.objects.filter(status='APPROVED')  # HARDCODED: Only show APPROVED leaves on calendar
    for leave in approved_leaves:
        events.append({
            'title': f"{leave.user.first_name} ({leave.get_leave_type_display()})",
            'start': leave.start_date.isoformat(),
            'end': (leave.end_date).isoformat(), # FullCalendar is usually exclusive end, but simple view usually fine.
            # HARDCODED: Calendar color scheme - green (#28a745) for ANNUAL leave, yellow (#ffc107) for others
            'color': '#28a745' if leave.leave_type == 'ANNUAL' else '#ffc107',
        })
    return JsonResponse(events, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'core/calendar.html')
