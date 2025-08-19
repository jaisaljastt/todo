from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('home/', views.home_view, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.LogoutView, name='logout'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/resend/', views.resend_password_reset_email, name='password_reset_resend'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password/check-inbox.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password/reset-password.html'), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='password/password-reset-success.html'), name='password_reset_complete'),

    path('api/tasks/', views.get_tasks, name='get-tasks'),
    path('api/tasks/create/', views.create_task, name='create-task'),
    path('api/tasks/<int:task_id>/update/', views.update_task, name='update-task'),
    path('api/tasks/<int:task_id>/delete/', views.delete_task, name='delete-task'),
]