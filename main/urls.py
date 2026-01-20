from django.urls import path
from .views import HomePageView, LoginView, LogoutView, RegisterView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Resident dashboard
    path('resident/', views.resident, name='resident'),

    # Emergency
    path('submit-report/', views.submit_emergency_report, name='submit_report'),
    path('emergency-reports/', views.emergency_report, name='emergency_reports'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),

    # Notifications
    path('notifications/', views.notification, name='notifications'),

    # Responders & contacts
    path('responders/', views.emergency_responder, name='responders'),
    path('contacts/', views.contact_assignment, name='contacts'),

    # AJAX
    path('ajax/unread-notifications/', views.unread_notifications_ajax, name='unread_notifications'),
]

