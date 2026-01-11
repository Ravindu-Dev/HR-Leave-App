from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manager/', views.manager_dashboard_view, name='manager_dashboard'),
    path('leave/<int:leave_id>/approve/', views.approve_leave, name='approve_leave'),
    path('leave/<int:leave_id>/reject/', views.reject_leave, name='reject_leave'),
    path('leave/<int:leave_id>/download/', views.download_permission_letter, name='download_permission_letter'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/calendar/', views.calendar_api, name='calendar_api'),
]
