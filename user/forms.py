from django import forms
from .models import *


class CaseCreationForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["case_number","domain","link"]