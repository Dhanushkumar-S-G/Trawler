from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),    
    path("scan/", scan, name="scan"),
    path("trawler/<str:case_number>/",trawler, name="trawler"),
    path("email_header_analyse/",analyse_header,name="email-header-analyse"),
    path("malware_analysis/",malware_analysis,name="malware-analysis"),
    path("mobile_search/",mobile_search,name="mobile-search"),
    path("mobile_search/<str:case_num>",mobile_details,name="mobile-details"),
    path("casedetails/",create_case,name='create-case'),
    path("upload_dump",upload_dump,name="upload-dump"),
    path("upi_recon/",upi_recon,name="upi-recon"),
    path("name_lookup/",name_lookup,name="name-lookup"),
    path("name_lookup/<str:case_num>",name_lookup_details,name="name-lookup-details"),
    path("twitter_lookup/",twitter_details,name="twitter-details"),
    path("dump_analysis/",dump_analysis,name='dump-analysis'),
    path("email_lookup/",email_lookup,name='email-lookup')
]


