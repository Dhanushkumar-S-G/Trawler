from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),    
    path("scan/", scan, name="scan"),
    path("gods_eye/",gods_eye, name="gods-eye")
]