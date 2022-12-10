from django.shortcuts import render,redirect
from .forms import *
from email.parser import HeaderParser
import time
import dateutil.parser

from datetime import datetime
import re


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


def dateParser(line):
    try:
        r = dateutil.parser.parse(line, fuzzy=True)
    except ValueError:
        r = re.findall('^(.*?)\s*(?:\(|utc)', line, re.I)
        if r:
            r = dateutil.parser.parse(r[0])
    return r


def utility_processor():
    def getCountryForIP(line):
        ipv4_address = re.compile(r"""
            \b((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.
            (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d))\b""", re.X)
        ip = ipv4_address.findall(line)
        if ip:
            ip = ip[0]  # take the 1st ip and ignore the rest
            if IP(ip).iptype() == 'PUBLIC':
                r = reader.country(ip).country
                if r.iso_code and r.name:
                    return {
                        'iso_code': r.iso_code.lower(),
                        'country_name': r.name
                    }
    return dict(country=getCountryForIP)

def getHeaderVal(h, data, rex='\s*(.*?)\n\S+:\s'):
    r = re.findall('%s:%s' % (h, rex), data, re.X | re.DOTALL | re.I)
    if r:
        return r[0].strip()
    else:
        return None
    

def email_header(header):
    mail_data = header
    r = {}
    n = HeaderParser().parsestr(mail_data)
    received = n.get_all('Received')
    if received:
        received = [i for i in received if ('from' in i or 'by' in i)]
    else:
        received = re.findall(
            'Received:\s*(.*?)\n\S+:\s+', mail_data, re.X | re.DOTALL | re.I)
    c = len(received)
    for i in range(len(received)):
        if ';' in received[i]:
            line = received[i].split(';')
        else:
            line = received[i].split('\r\n')
        line = list(map(str.strip, line))
        line = [x.replace('\r\n', ' ') for x in line]
        try:
            if ';' in received[i + 1]:
                next_line = received[i + 1].split(';')
            else:
                next_line = received[i + 1].split('\r\n')
            next_line = list(map(str.strip, next_line))
            next_line = [x.replace('\r\n', '') for x in next_line]
        except IndexError:
            next_line = None


        if line[0].startswith('from'):
            data = re.findall(
                """
                from\s+
                (.*?)\s+
                by(.*?)
                (?:
                    (?:with|via)
                    (.*?)
                    (?:\sid\s|$)
                    |\sid\s|$
                )""", line[0], re.DOTALL | re.X)
        else:
            data = re.findall(
                """
                ()by
                (.*?)
                (?:
                    (?:with|via)
                    (.*?)
                    (?:\sid\s|$)
                    |\sid\s
                )""", line[0], re.DOTALL | re.X)


    summary = {
        'From': n.get('From') or getHeaderVal('from', mail_data),
        'To': n.get('to') or getHeaderVal('to', mail_data),
        'Cc': n.get('cc') or getHeaderVal('cc', mail_data),
        'Subject': n.get('Subject') or getHeaderVal('Subject', mail_data),
        'MessageID': n.get('Message-ID') or getHeaderVal('Message-ID', mail_data),
        'Date': n.get('Date') or getHeaderVal('Date', mail_data),
    }
    ips = set(re.findall( r'[0-9]+(?:\.[0-9]+){3}', mail_data ))
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", mail_data)
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex,mail_data) 
    
    security_headers = ['Received-SPF', 'Authentication-Results',
                        'DKIM-Signature', 'ARC-Authentication-Results']
    
    data = {
        "ips":ips,
        "emails":emails,
        "urls":urls,
        "security_headers":security_headers,
        "summary":summary,
        "n":n
    }
    return data
    
    



def analyse_header(request):
    if request.method == "POST":
        header = request.POST.get("header")
        data = email_header(header)
        print("asdfasdfasdf",type(data["n"]))
        return render(request,"user/analyse_header.html",{
            "summary": data["summary"],
            "ips":data["ips"],
            "urls":data["urls"],
            "emails":set(data["emails"]),
            "is_true":True

        })
    return render(request,"user/analyse_header.html")

import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi
import subprocess
import json
def malware_analysis(request):
    if request.method == "POST":
        print(request.FILES)
        form = MalwareUploadForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            case_number = form.cleaned_data.get("case_number")
            file = form.cleaned_data.get("malware_file")
            case_obj = Case.objects.get(case_number=case_number)
            mal_obj = MalwareFile.objects.create(case_obj=case_obj,malware_file = file)
            mal_obj.save()
            file_type_output = subprocess.run(["/media/dhanush/COLLEGE/godseye/user/filetype.sh",mal_obj.malware_file.path],capture_output=True)
            file_type_output = file_type_output.stdout
            file_type_output = file_type_output.decode('ascii')

            
            hashing_output = subprocess.run(["/media/dhanush/COLLEGE/godseye/user/hashing.sh",mal_obj.malware_file.path],capture_output=True)
            hashing_output = hashing_output.stdout
            hashing_output = hashing_output.decode('ascii')

            hash_ = hashing_output[10:51]
            
            import hashlib
            from virus_total_apis import PublicApi as VirusTotalPublicApi
            API_KEY = "544563dd7491894b32d1a605d3358ec23a8ed72b56968af6eb1565e52cc43ef1"
            EICAR = hash_.encode('utf-8')
            EICAR_SHA1 = hashlib.sha1(EICAR).hexdigest()
            vt = VirusTotalPublicApi(API_KEY)   

            response = vt.get_file_report(EICAR_SHA1)
            virus_total = json.dumps(response, sort_keys=False, indent=4)
            form = MalwareUploadForm()
            return render(request,"user/malware_analysis.html",{
        "form":form,"file_type_output":file_type_output,"hashing_output":hashing_output,"is_true":True,"virus_total":virus_total
    })            

    form = MalwareUploadForm()

    return render(request,"user/malware_analysis.html",{
        "form":form
    })