from django.shortcuts import render, redirect, get_object_or_404
from .models import Resident, Alert, EmergencyResponder, ContactAssignment, EmergencyReport,  Notification
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .forms import EmergencyReportForm, ResidentRegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.decorators import login_required
from .forms import EmergencyReportForm
from django.contrib import messages

def notification(request):
    return render(request, 'main/notification.html')

# ----------------------------
# Home page
# ----------------------------

def home(request):
    reports_count = EmergencyReport.objects.count()
    notifications_count = Notification.objects.count()
    return render(request, "main/home.html", {
        "reports_count": reports_count,
        "notifications_count": notifications_count,
    })

class HomePageView(TemplateView):
    template_name = 'main/home.html'  # Make sure you have this template

# For login/logout
class LoginView(AuthLoginView):
    template_name = 'main/login.html'

class LogoutView(AuthLogoutView):
    next_page = '/'  # redirect after logout

class RegisterView(CreateView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

# -----------------------------
# Registration View
# -----------------------------
def register(request):
    if request.method == 'POST':
        form = ResidentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Resident automatically
            Resident.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            login(request, user)
            return redirect('resident')
    else:
        form = ResidentRegisterForm()
    return render(request, 'main/register.html', {'form': form})

# ----------------------------
# Resident Dashboard
# ----------------------------

@login_required
def resident(request):
    alerts = Alert.objects.all()  # safe after migration

    return render(request, 'main/resident.html', {
        'alerts': alerts,
        'notifications': [],
        'emergency_reports': [],
        'resident': request.user.resident
    })


@login_required
def notification(request):
    resident = resident = get_object_or_404(Resident, user=request.user)
    notifications = Notification.objects.filter(report__resident=resident).order_by('-created_at')
    return render(request, "main/notification.html", {
        "notifications": notifications,
    })

# ----------------------------
# Emergency Reports
# ----------------------------
@login_required
def emergency_report(request):
    reports = EmergencyReport.objects.all().order_by('-created_at')
    return render(request, "main/emergency_report.html", {"reports": reports})


@login_required
def report_detail(request, pk):
    report = redirect(EmergencyReport, pk=pk)
    notifications = Notification.objects.filter(report=report)
    return render(request, "main/report_detail.html", {"report": report, "notifications": notifications})


# ----------------------------
# Contacts & Responders
# ----------------------------
@login_required
def contact_assignment(request):
    contacts = ContactAssignment.objects.all()
    return render(request, "main/contact_assignment.html", {"contacts": contacts})


@login_required
def emergency_responder(request):
    responders = EmergencyResponder.objects.all()
    return render(request, "main/emergency_responder.html", {"responders": responders})


# ----------------------------
# AJAX: Unread Notifications
# ----------------------------
@login_required
def unread_notifications_ajax(request):
    resident = get_object_or_404(Resident, user=request.user)
    unread_count = Notification.objects.filter(report__resident=resident).count()
    return JsonResponse({'unread_count': unread_count})

# ----------------------------
# EMERGENCY REPORT
# ----------------------------
@login_required
def submit_emergency_report(request):
    try:
        resident_obj = Resident.objects.get(user=request.user)
    except Resident.DoesNotExist:
        messages.error(request, "Resident profile not found.")
        return redirect('resident')  # dashboard

    if request.method == "POST":
        report_type = request.POST.get('type')
        description = request.POST.get('description')

        if not report_type or not description:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'main/submit_report.html', {'resident': resident_obj})

        # Create emergency report
        report = EmergencyReport.objects.create(
            resident=resident_obj,  # Resident instance
            type=report_type,
            description=description,
            status='Pending'
        )

        # Create notification
        Notification.objects.create(
            resident=resident_obj,  # ✅ MUST be Resident
            message=f"Your emergency report ({report_type}) has been submitted.",
            report=report,
            sent_via="System"
        )

        messages.success(request, "Emergency report submitted successfully!")
        return redirect('resident')

    return render(request, 'main/submit_report.html', {'resident': resident_obj})
