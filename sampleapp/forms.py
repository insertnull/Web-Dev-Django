from django import forms
from .models import *

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'