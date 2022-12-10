from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),    
    path("scan/", scan, name="scan"),
    path("spoor/<str:case_number>",spoor, name="spoor"),
    path("email_header_analyse",analyse_header,name="email-header-analyse"),
    path("malware_analysis",malware_analysis,name="malware-analysis")
]