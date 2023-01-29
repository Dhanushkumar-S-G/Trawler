from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),    
    path("scan/", scan, name="scan"),
    path("trawler/<str:case_number>/",trawler, name="trawler"),
    path("email_header_analyse/",analyse_header,name="email-header-analyse"),
    path("malware_analysis/",malware_analysis,name="malware-analysis"),
    path("mobile_search/",mobile_search,name="mobile-search"),
]