from django import forms
from .models import Booking, LabBooking


# 🎓 Student Equipment Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'equipment',
            'name',
            'student_class',
            'roll',
            'pin',
            'quantity',
            'booking_date',
            'booking_time',
            'duration',
            'purpose'
        ]

        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'student_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Class'}),
            'roll': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll'}),
            'pin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter PIN'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Purpose (optional)', 'rows': 3}),
        }


# 🏫 Teacher Lab Booking Form
class LabBookingForm(forms.ModelForm):
    class Meta:
        model = LabBooking
        fields = '__all__'

        widgets = {
            'lab': forms.Select(attrs={'class': 'form-control'}),
            'teacher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Teacher Name'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }