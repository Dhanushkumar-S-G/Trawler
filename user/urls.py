from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),    
    path("scan/", scan, name="scan"),
    path("spoor/<str:case_number>",spoor, name="spoor")
]