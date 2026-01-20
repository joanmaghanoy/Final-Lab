from django.contrib import admin
from .models import (
    Resident,
    EmergencyResponder,
    ContactAssignment,
    EmergencyReport,
    Notification
)


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'address', 'created_at')
    search_fields = ('user__username', 'phone', 'address')

    def username(self, obj):
        return obj.user.username

    username.short_description = 'Username'


@admin.register(EmergencyResponder)
class ResponderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type',)


@admin.register(ContactAssignment)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('responder', 'contact_number', 'barangay_area')
    list_filter = ('barangay_area', 'responder')


@admin.register(EmergencyReport)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'resident', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('type', 'resident__user__username', 'description')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('report', 'sent_via', 'created_at')
    list_filter = ('sent_via',)
    search_fields = ('report__type', 'message')