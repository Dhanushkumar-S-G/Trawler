from django.shortcuts import render,redirect
from .forms import *

def dashboard(request):
    return render(request,"user/index.html")


def scan(request):
    if request.method == "POST":
        form = CaseCreationForm(request.POST)
        print("haidfasd", form.is_valid())
        if form.is_valid():
            form.save()
            case_number = form.cleaned_data["case_number"]
            return redirect("spoor",case_number)
        else:
            case_number = request.POST.get("case_number")
            return redirect("spoor",case_number)
    form = CaseCreationForm()
    return render(request, "user/scan.html",{
        "form":form
    })


def spoor(request,case_number):
    case_obj = Case.objects.get(case_number = case_number)
    return render(request,"user/spoor.html",{
        "domain": str(case_obj.domain),
        "url":str(case_obj.link),
        "case_number":case_obj.case_number
    })