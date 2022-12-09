from django.shortcuts import render,redirect
from .forms import *

def dashboard(request):
    return render(request,"user/index.html")


def scan(request):
    if request.method == "POST":
        form = CaseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gods-eye")
    form = CaseCreationForm()
    return render(request, "user/scan.html",{
        "form":form
    })


def gods_eye(request):
    return render(request,"user/gods_eye.html")