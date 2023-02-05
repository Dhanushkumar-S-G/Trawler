from django.db import models

class Case(models.Model):
    case_number = models.CharField(max_length=5,unique=True)
    domain = models.CharField(max_length=50,null=True,blank=True)
    link = models.CharField(max_length=255,null=True,blank=True)
    is_family = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=20,null=True,blank=True)
    

class WhoIs(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_whois_details")
    res = models.JSONField(null=True,blank=True)


class SslCertificate(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_sslcertificate_details")
    res = models.JSONField(null=True,blank=True)


class WappalyzerModel(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_wappalyzer_details")
    res = models.JSONField(null=True,blank=True)


class NmapPort(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_nmap_port_details")
    res = models.JSONField(null=True,blank=True)


class DnsEnum(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_dns_enum_details")
    res = models.JSONField(null=True,blank=True)


class SubDomain(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_subdomain_details")
    res = models.JSONField(null=True,blank=True)
    
            
class WhatCms(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_whatcms_details")
    res = models.JSONField(null=True,blank=True)
                

class MalwareFile(models.Model):
    case_obj = models.ForeignKey(Case,on_delete=models.CASCADE,related_name="related_malware_files")
    malware_file = models.FileField(upload_to="media/")
    
class OsScan(models.Model):
    case_obj = models.OneToOneField(Case,on_delete=models.CASCADE,related_name="related_os_scan_details")
    res = models.JSONField(null=True,blank=True)


# class Trawler(models.Model):
#     case_num = models.IntegerField(unique=True)
#     mobile_number = models.CharField(max_length=10)
#     email = models.EmailField()


class DumpData(models.Model):
    case_number = models.CharField(max_length=20,unique=True)
    file = models.FileField(upload_to="dump_file/")



class CaseDetails(models.Model):
    case_num = models.CharField(max_length=20,unique=True)
    phonenumber = models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    phonenumber_suspect_count = models.TextField(null=True,blank=True)
    email_suspect_count = models.TextField(null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    upiid = models.TextField(null=True,blank=True)
    location = models.TextField(null=True,blank=True)
    phone_number_owner =models.TextField(null=True,blank=True)
    phone_number_owner_location = models.TextField(null=True,blank=True)
    is_whatsapp_active = models.BooleanField(default=False)
    is_breached = models.BooleanField(default=False)
    breached_data = models.TextField(null=True,blank=True)
    upiid_name = models.TextField(null=True,blank=True)
    is_upi_verified =models.BooleanField(default=False)


class ReverseNumberLookup(models.Model):
    phonenumber = models.CharField(max_length=10)
    casedetail = models.ForeignKey(CaseDetails,on_delete=models.CASCADE)
    numberlookup = models.TextField(null=True,blank=True)


class NameLookUpDetails(models.Model):
    username = models.CharField(max_length=50)
    casedetail = models.ForeignKey(CaseDetails,on_delete=models.CASCADE)
    namelookup = models.TextField(null=True,blank=True)