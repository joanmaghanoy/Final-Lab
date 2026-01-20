from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmergencyReport

class ResidentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)

class EmergencyReportForm(forms.ModelForm):
    class Meta:
        model = EmergencyReport
        fields = ['type', 'description']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Report Type'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your report'}),
        }
