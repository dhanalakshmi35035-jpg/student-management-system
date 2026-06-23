from django import forms
from .models import Student, Attendance,Mark,Fee


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'department', 'email']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'Sensors', 'IndustrialInstrumentation', 'ProcessControl']   

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'total_fee', 'paid_fee']         