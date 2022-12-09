from rest_framework import routers, serializers, viewsets
from user.models import *

class WhoIsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoIs
        fields = "__all__"


class SslCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SslCertificate
        fields = "__all__"


class WappalyzerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WappalyzerModel
        fields = "__all__"

    
class NmapPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = NmapPort
        fields = "__all__"


class DnsEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnsEnum
        fields = "__all__"


class SubDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDomain
        fields = "__all__"
        

class WhatCmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatCms
        fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"


class OsScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = OsScan
        fields = "__all__"