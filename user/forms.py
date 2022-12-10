from django import forms
from .models import *


class CaseCreationForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["case_number","domain","link"]


class MalwareUploadForm(forms.Form):
    case_number = forms.CharField(max_length=5)
    malware_file = forms.FileField()