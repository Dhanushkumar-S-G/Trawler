from django.urls import path
from .views import *

urlpatterns = [
    path("getip/",get_ip,name="api-getip"),
    path("whois/",whois,name="api-whois"),
    path("ssl_certificate/",ssl_certificate, name="api-ssl-certificate"),
    path("wappalyzer/",wappalyzer,name="api-wappalyzer"),
    path("nmap_port/",nmap_port,name="api-nmap"),
    path("dns_enum/",dns_enum,name="api-dns-enum"),
    path("dns_for_family/",dns_for_family,name="api-dns-for-family"),
    path("subdomain_enum/",subdomain_enum,name="api-subdomain-enum"),   
    path("os_scan/",osscan,name="api-os-scan"),
    path("check_whatsapp/",check_whatsapp, name="api-check-whatsapp"),
    path("check_number_owner/",check_number_owner,name="api-check-number-owner"),
    path("number_lookup/",number_lookup,name="api-number-lookup"),
    path("search_breached_data/",search_breached_data,name="api-search-breached-data"),
    path("name_lookup/",name_lookup,name="api-name-lookup"),
    path("upi_enum/",upi_enum,name="api-upi-enum"),
    path("check_amazon/",check_amazon,name="check-amazon"),
    path("get_dump/",get_dump,name="get-dump"),
    path("get_insta_bio",get_insta_bio,name='get-insta-bio'),
    path("get_twitter_bio",get_twitter_bio,name="get-twitter-bio"),
    path("get_email_lookup/",email_lookup, name='get-email-lookup'),

    # path()
] 