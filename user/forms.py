from django import forms
from .models import *


class CaseCreationForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = "__all__"