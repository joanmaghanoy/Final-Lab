from django.db import models
from django.contrib.auth.models import User

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Alert(models.Model):
    resident = models.ForeignKey(
        Resident,
        on_delete=models.CASCADE,
        related_name='alerts',
        null=True,
        blank=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class Notification(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    report = models.ForeignKey('EmergencyReport', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    sent_via = models.CharField(max_length=10, choices=[('sms','SMS'),('email','Email'),('app','App')], default='app')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class EmergencyReport(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class EmergencyResponder(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactAssignment(models.Model):
    responder = models.ForeignKey(EmergencyResponder, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    barangay_area = models.CharField(max_length=100)

alerts = Alert.objects.none()
notifications = Notification.objects.none()
emergency_reports = EmergencyReport.objects.none()
