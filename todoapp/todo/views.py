from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Task
import json

from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm

# ... (keep existing login/register/logout views)

@login_required
def home_view(request):
    return render(request, 'home/index.html')

@login_required
def get_tasks(request):
    """API endpoint to get tasks for the logged-in user"""
    date = request.GET.get('date')
    if date:
        tasks = Task.objects.filter(user=request.user, date=date)
    else:
        tasks = Task.objects.filter(user=request.user, date=timezone.now().date())
    
    task_list = [{
        'id': task.id,
        'text': task.text,
        'status': task.status,
        'date': task.date.strftime('%Y-%m-%d')
    } for task in tasks]
    
    return JsonResponse({'tasks': task_list})

@login_required
@csrf_exempt
def create_task(request):
    """API endpoint to create a new task"""
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            user=request.user,
            text=data['text'],
            status=data.get('status', 'todo'),
            date=parse_date(data['date'])
        )
        return JsonResponse({
            'id': task.id,
            'text': task.text,
            'status': task.status,
            'date': task.date.strftime('%Y-%m-%d')
        })

@login_required
@csrf_exempt
def update_task(request, task_id):
    """API endpoint to update a task"""
    if request.method == 'PUT':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        data = json.loads(request.body)
        task.status = data.get('status', task.status)
        task.save()
        return JsonResponse({'success': True})

@login_required
@csrf_exempt
def delete_task(request, task_id):
    """API endpoint to delete a task"""
    if request.method == 'DELETE':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({'success': True})


# Create your views here.
def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home')  # Redirect to home or another page after login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login/login.html')

def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home-page')
    if request.method == 'POST':
        # Handle registration logic here
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'User successfully created, login now')
        return redirect('login')


    return render(request, 'register/register.html')

def LogoutView(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password/forgot-password.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "No account found with this email.")
            return redirect('password_reset')  # redirect back to the reset page

        # If email exists, save to session
        self.request.session['reset_email'] = email

        # Continue with normal flow (sending reset email, redirecting, etc.)
        return super().form_valid(form)
    
def resend_password_reset_email(request):
    email = request.session.get('reset_email')
    if email:
        # Check if a user with this email exists
        if not User.objects.filter(email=email).exists():
            messages.error(request, "No user is associated with this email address.")
            return redirect('password_reset')
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
            )
            messages.success(request, "Password reset email resent.")
    else:
        messages.error(request, "No email found in session.")
        return redirect('password_reset')
    return redirect('password_reset_done')