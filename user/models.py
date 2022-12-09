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
    