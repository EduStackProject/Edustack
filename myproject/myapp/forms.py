# core/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'grade','phno'] 
     
class RollNumberForm(forms.Form):
    roll_number = forms.CharField(label='Enter Roll Number')
