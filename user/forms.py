from django import forms
from .models import *

class CaseCreationForm(forms.ModelForm):
    class Meta:
        model = Case
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control'}),
            'domain': forms.TextInput(attrs={'class':'form-control'}),
            'link' : forms.TextInput(attrs={'class':'form-control'})
        }
        fields = ["case_number","domain","link"]


class MalwareUploadForm(forms.Form):
    case_number = forms.CharField(max_length=5)
    malware_file = forms.FileField()


class DumpFileUploadForm(forms.ModelForm):
    class Meta:
        model = DumpData
        widgets = {
            'case_number': forms.TextInput(attrs={'class': 'form-control'})
        }
        fields = ["case_number","file"]


class CaseDetailsForm(forms.ModelForm):
    class Meta:
        widgets = {
            'case_num': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber' : forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }
        model = CaseDetails
        fields = ('case_num','phonenumber','email')

        