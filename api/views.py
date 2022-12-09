from Wappalyzer import Wappalyzer, WebPage
from django.shortcuts import render
from django.http import JsonResponse
from user.models import *
from .serializers import *
from pycrtsh import Crtsh
import dns.resolver
import requests
import nmap
import socket
import json
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


def get_ip(request):
    case_number = request.GET.get("case_number",None)
    domain = request.GET.get("domain",None)
    ip_address = socket.gethostbyname(domain)
    if case_number in [None ,'']:
        return JsonResponse({"ip_adrdess":ip_address})
    else:
        case_obj = Case.objects.get(case_number=case_number)
        case_obj.ip_address = ip_address
        case_obj.save()
        return JsonResponse({"ip_address":ip_address})
        


def whois(request):
    ip_address = request.GET.get("ip_address",None)
    case_number = request.GET.get("case_number",None)
    if case_number in [None , '']:
        base_url1 = "https://ipapi.co/"
        base_url2 = "/json/"
        api_url = base_url1 + str(ip_address) + base_url2
        response = requests.get(api_url)
        data = response.json()
        return JsonResponse(data=data)
    else:
        case_obj = Case.objects.get(case_number = case_number)
        whois_obj, created = WhoIs.objects.get_or_create(case_obj=case_obj)
        if created:
            base_url1 = "https://ipapi.co/"
            base_url2 = "/json/"
            api_url = base_url1 + str(ip_address) + base_url2
            response = requests.get(api_url)
            data = response.json()
            whois_obj.res = data
            whois_obj.save() 
        serialized_data = WhoIsSerializer(whois_obj).data
        print(serialized_data)
        return JsonResponse(serialized_data)





def ssl_certificate(request):
    domain = request.GET.get("domain",None)
    case_number = request.GET.get("case_number",None)
    if case_number in [None , ""]:
        c = Crtsh()
        certs = c.search(domain)
        case_number = request.GET.get("case_number",None)
        return JsonResponse({"ssl_certificate": certs})
    else:
        case_obj = Case.objects.get(case_number = case_number)
        ssl_obj, created = SslCertificate.objects.get_or_create(case_obj = case_obj)
        if created:
            c = Crtsh()
            ssl_obj.res = json.loads(json.dumps({"ssl_certificate" :c.search(domain)},cls=DateTimeEncoder))
            ssl_obj.save()
        
        serialized_data = SslCertificateSerializer(ssl_obj).data
        return JsonResponse(data=serialized_data)
    


def wappalyzer(request):
    case_number = request.GET.get("case_number",None)
    url = request.GET.get("url",None)
    if case_number in [None, '']:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(url)
        stack = wappalyzer.analyze_with_versions_and_categories(webpage)
        return JsonResponse(stack)
    else:
        case_obj = Case.objects.get(case_number = case_number)
        wapp_obj, created  = WappalyzerModel.objects.get_or_create(case_obj=case_obj)
        if created:
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_url(url)
            stack = wappalyzer.analyze_with_versions_and_categories(webpage)
            wapp_obj.res = stack
            wapp_obj.save()
        serialized_data = WappalyzerModelSerializer(wapp_obj).data
        return JsonResponse(data=serialized_data)




def nmap_port(request):
    case_number = request.GET.get("case_number",None)
    ip_address = request.GET.get("ip_address",None)
    if case_number in [None, ""]:
        port=[20,21,22,23,25,53,80,110,119,123,143,161,194,443]
        target = ip_address
        scanner = nmap.PortScanner()
        results =dict()
        for i in port:
            res = scanner.scan(target, str(i))
            res = res['scan'][target]['tcp'][i]['state']
            results[i] = res
        return JsonResponse(results)
    else:
        case_obj = Case.objects.get(case_number = case_number)
        nmap_obj, created = NmapPort.objects.get_or_create(case_obj=case_obj)
        if created:
            port=[20,21,22,23,25,53,80,110,119,123,143,161,194,443]
            target = ip_address
            scanner = nmap.PortScanner()
            results =dict()
            for i in port:
                res = scanner.scan(target, str(i))
                res = res['scan'][target]['tcp'][i]['state']
                results[i] = res
            nmap_obj.res = results
            nmap_obj.save()
        
        serialized_data = NmapPortSerializer(nmap_obj).data
        return JsonResponse(data=serialized_data)
        


def dns_enum(request):
    case_number = request.GET.get("case_number",None)
    domain = request.GET.get("domain",None)
    if case_number in ['',None]:  
        record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']
        record_val = {}
        i = 0
        for records in record_types:
            try:
                record = []
                answer = dns.resolver.resolve(domain, records)
                for server in answer:
                    record.append(server.to_text())
                record_val[records] = record
                i += 1

            except dns.resolver.NoAnswer:
                    pass
            except dns.resolver.NXDOMAIN:
                    pass
            except KeyboardInterrupt:
                    pass

        return JsonResponse(record_val)
    else:
        case_obj = Case.objects.get(case_number = case_number)
        dns_obj, created = DnsEnum.objects.get_or_create(case_obj = case_obj)
        if created:
            record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']
            record_val = {}
            i = 0
            for records in record_types:
                try:
                    record = []
                    answer = dns.resolver.resolve(domain, records)
                    for server in answer:
                        record.append(server.to_text())
                    record_val[records] = record
                    i += 1

                except dns.resolver.NoAnswer:
                        pass
                except dns.resolver.NXDOMAIN:
                        pass
                except KeyboardInterrupt:
                        pass
            dns_obj.res = record_val
            dns_obj.save()
        serialized_data = DnsEnumSerializer(dns_obj).data
        return JsonResponse(data=serialized_data)




    
def dns_for_family(request):
    case_number = request.GET.get("case_number",None)
    domain = request.GET.get("domain",None)
    base_url = "https://dnsforfamily.com/api/checkHost?hostnames[]="

    final_url = base_url+domain

    r = requests.get(final_url)
    data = r.json()
    
    if case_number not in ['',None]:
        case_obj = Case.objects.get(case_number = case_number)
        case_obj.is_family = data["result"][domain]
        case_obj.save()

    return JsonResponse(data)  



def subdomain_enum(request):
    case_number = request.GET.get("case_number",None)
    domain = request.GET.get("domain",None)
    if case_number in ['',None]:
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ['1.1.1.1']
        subdomain_array = ['www','mail','ftp','localhost','webmail','smtp','pop','ns1','webdisk','ns2','cpanel','whm','autodiscover','autoconfig','m','imap','test','ns','blog','pop3','dev','www2','admin','forum','news','vpn','ns3','mail2','new','mysql','old','lists','support','mobile','mx','static','docs','beta','shop','sql','secure','demo','cp','calendar','wiki','web','media','email','images','img','www1','intranet','portal','video','sip','dns2','api','cdn','stats','dns1','ns4','www3','dns','search','staging','server','mx1','chat','wap','my','svn','mail1','sites','proxy','ads','host','crm','cms','backup','mx2','lyncdiscover','info','apps','download','remote','db','forums','store','relay','files','newsletter','app','live','owa','en','start','sms','office','exchange','ipv4','mail3','help','blogs','helpdesk','web1','home','library','ftp2','ntp','monitor','login','service','correo','www4','moodle','it','gateway','gw','i','stat','stage','ldap','tv','ssl','web2','ns5','upload','nagios','smtp2','online','ad','survey','data','radio','extranet','test2','mssql','dns3','jobs','services','panel','irc','hosting','cloud','de','gmail','s','bbs','cs','ww','mrtg','git','image','members','poczta','s1','meet','preview','fr','cloudflare-resolve-to','dev2','photo','jabber','legacy','go','es','ssh','redmine','partner','vps','server1','sv','ns6','webmail2','av','community','cacti','time','sftp','lib','facebook','www5','smtp1','feeds','w','games','ts','alumni','dl','s2','phpmyadmin','archive','cn','tools','stream','projects','elearning','im','iphone','control','voip','test1','ws','rss','sp','wwww','vpn2','jira','list','connect','gallery','billing','mailer','update','pda','game','ns0','testing','sandbox','job','events','dialin','ml','fb','videos','music','a','partners','mailhost','downloads','reports','ca','router','speedtest','local','training','edu','bugs','manage','s3','status','host2','ww2','marketing','conference','content','network-ip','broadcast-ip','english','catalog','msoid','mailadmin','pay','access','streaming','project','t','sso','alpha','photos','staff','e','auth','v2','web5','web3','mail4','devel','post','us','images2','master','rt','ftp1','qa','wp','dns4','www6','ru','student','w3','citrix','trac','doc','img2','css','mx3','adm','web4','hr','mailserver','travel','sharepoint','sport','member','bb','agenda','link','server2','vod','uk','fw','promo','vip','noc','design','temp','gate','ns7','file','ms','map','cache','painel','js','event','mailing','db1','c','auto','img1','vpn1','business','mirror','share','cdn2','site','maps','tickets','tracker','domains','club','images1','zimbra','cvs','b2b','oa','intra','zabbix','ns8','assets','main','spam','lms','social','faq','feedback','loopback','groups','m2','cas','loghost','xml','nl','research','art','munin','dev1','gis','sales','images3','report','google','idp','cisco','careers','seo','dc','lab','d','firewall','fs','eng','ann','mail01','mantis','v','affiliates','webconf','track','ticket','pm','db2','b','clients','tech','erp','monitoring','cdn1','images4','payment','origin','client','foto','domain','pt','pma','directory','cc','public','finance','ns11','test3','wordpress','corp','sslvpn','cal','mailman','book','ip','zeus','ns10','hermes','storage','free','static1','pbx','banner','mobil','kb','mail5','direct','ipfixe','wifi','development','board','ns01','st','reviews','radius','pro','atlas','links','in','oldmail','register','s4','images6','static2','id','shopping','drupal','analytics','m1','images5','images7','img3','mx01','www7','redirect','sitebuilder','smtp3','adserver','net','user','forms','outlook','press','vc','health','work','mb','mm','f','pgsql','jp','sports','preprod','g','p','mdm','ar','lync','market','dbadmin','barracuda','affiliate','mars','users','images8','biblioteca','mc','ns12','math','ntp1','web01','software','pr','jupiter','labs','linux','sc','love','fax','php','lp','tracking','thumbs','up','tw','campus','reg','digital','demo2','da','tr','otrs','web6','ns02','mailgw','education','order','piwik','banners','rs','se','venus','internal','webservices','cm','whois','sync','lb','is','code','click','w2','bugzilla','virtual','origin-www','top','customer','pub','hotel','openx','log','uat','cdn3','images0','cgi','posta','reseller','soft','movie','mba','n','r','developer','nms','ns9','webcam','construtor','ebook','ftp3','join','dashboard','bi','wpad','admin2','agent','wm','books','joomla','hotels','ezproxy','ds','sa','katalog','team','emkt','antispam','adv','mercury','flash','myadmin','sklep','newsite','law','pl','ntp2','x','srv1','mp3','archives','proxy2','ps','pic','ir','orion','srv','mt','ocs','server3','meeting','v1','delta','titan','manager','subscribe','develop','wsus','oascentral','mobi','people','galleries','wwwtest','backoffice','sg','repo','soporte','www8','eu','ead','students','hq','awstats','ec','security','school','corporate','podcast','vote','conf','magento','mx4','webservice','tour','s5','power','correio','mon','mobilemail','weather','international','prod','account','xx','pages','pgadmin','bfn2','webserver','www-test','maintenance','me','magazine','syslog','int','view','enews','ci','au','mis','dev3','pdf','mailgate','v3','ss','internet','host1','smtp01','journal','wireless','opac','w1','signup','database','demo1','br','android','career','listserv','bt','spb','cam','contacts','webtest','resources','1','life','mail6','transfer','app1','confluence','controlpanel','secure2','puppet','classifieds','tunet','edge','biz','host3','red','newmail','mx02','sb','physics','ap','epaper','sts','proxy1','ww1','stg','sd','science','star','www9','phoenix','pluto','webdav','booking','eshop','edit','panelstats','xmpp','food','cert','adfs','mail02','cat','edm','vcenter','mysql2','sun','phone','surveys','smart','system','twitter','updates','webmail1','logs','sitedefender','as','cbf1','sugar','contact','vm','ipad','traffic','dm','saturn','bo','network','ac','ns13','webdev','libguides','asp','tm','core','mms','abc','scripts','fm','sm','test4','nas','newsletters','rsc','cluster','learn','panelstatsmail','lb1','usa','apollo','pre','terminal','l','tc','movies','sh','fms','dms','z','base','jwc','gs','kvm','bfn1','card','web02','lg','editor','metrics','feed','repository','asterisk','sns','global','counter','ch','sistemas','pc','china','u','payments','ma','pics','www10','e-learning','auction','hub','sf','cbf8','forum2','ns14','app2','passport','hd','talk','ex','debian','ct','rc','2012','imap4','blog2','ce','sk','relay2','green','print','geo','multimedia','iptv','backup2','webapps','audio','ro','smtp4','pg','ldap2','backend','profile','oldwww','drive','bill','listas','orders','win','mag','apply','bounce','mta','hp','suporte','dir','pa','sys','mx0','ems','antivirus','web8','inside','play','nic','welcome','premium','exam','sub','cz','omega','boutique','pp','management','planet','ww3','orange','c1','zzb','form','ecommerce','tmp','plus','openvpn','fw1','hk','owncloud','history','clientes','srv2','img4','open','registration','mp','blackboard','fc','static3','server4','s6','ecard','dspace','dns01','md','mcp','ares','spf','kms','intranet2','accounts','webapp','ask','rd','www-dev','gw2','mall','bg','teste','ldap1','real','m3','wave','movil','portal2','kids','gw1','ra','tienda','private','po','2013','cdn4','gps','km','ent','tt','ns21','at','athena','cbf2','webmail3','mob','matrix','ns15','send','lb2','pos','2','cl','renew','admissions','am','beta2','gamma','mx5','portfolio','contest','box','mg','wwwold','neptune','mac','pms','traveler','media2','studio','sw','imp','bs','alfa','cbf4','servicedesk','wmail','video2','switch','sam','sky','ee','widget','reklama','msn','paris','tms','th','vega','trade','intern','ext','oldsite','learning','group','f1','ns22','ns20','demo3','bm','dom','pe','annuaire','portail','graphics','iris','one','robot','ams','s7','foro','gaia','vpn3']

        subdomain_store = []
        for subdoms in subdomain_array:
            try:
                ip_value = dns.resolver.resolve(f'{subdoms}.{domain}', 'A')
                if ip_value:
                    subdomain_store.append(f'{subdoms}.{domain}')

            except dns.resolver.NXDOMAIN:
                pass

            except dns.resolver.NoAnswer:
                pass 
        return JsonResponse({"subdomain":subdomain_store})
    else:
        case_obj = Case.objects.get(case_number = case_number)
        sub_obj, created = SubDomain.objects.get_or_create(case_obj=case_obj)
        if created:
            dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
            dns.resolver.default_resolver.nameservers = ['1.1.1.1']
            subdomain_array = ['www','mail','ftp','localhost','webmail','smtp','pop','ns1','webdisk','ns2','cpanel','whm','autodiscover','autoconfig','m','imap','test','ns','blog','pop3','dev','www2','admin','forum','news','vpn','ns3','mail2','new','mysql','old','lists','support','mobile','mx','static','docs','beta','shop','sql','secure','demo','cp','calendar','wiki','web','media','email','images','img','www1','intranet','portal','video','sip','dns2','api','cdn','stats','dns1','ns4','www3','dns','search','staging','server','mx1','chat','wap','my','svn','mail1','sites','proxy','ads','host','crm','cms','backup','mx2','lyncdiscover','info','apps','download','remote','db','forums','store','relay','files','newsletter','app','live','owa','en','start','sms','office','exchange','ipv4','mail3','help','blogs','helpdesk','web1','home','library','ftp2','ntp','monitor','login','service','correo','www4','moodle','it','gateway','gw','i','stat','stage','ldap','tv','ssl','web2','ns5','upload','nagios','smtp2','online','ad','survey','data','radio','extranet','test2','mssql','dns3','jobs','services','panel','irc','hosting','cloud','de','gmail','s','bbs','cs','ww','mrtg','git','image','members','poczta','s1','meet','preview','fr','cloudflare-resolve-to','dev2','photo','jabber','legacy','go','es','ssh','redmine','partner','vps','server1','sv','ns6','webmail2','av','community','cacti','time','sftp','lib','facebook','www5','smtp1','feeds','w','games','ts','alumni','dl','s2','phpmyadmin','archive','cn','tools','stream','projects','elearning','im','iphone','control','voip','test1','ws','rss','sp','wwww','vpn2','jira','list','connect','gallery','billing','mailer','update','pda','game','ns0','testing','sandbox','job','events','dialin','ml','fb','videos','music','a','partners','mailhost','downloads','reports','ca','router','speedtest','local','training','edu','bugs','manage','s3','status','host2','ww2','marketing','conference','content','network-ip','broadcast-ip','english','catalog','msoid','mailadmin','pay','access','streaming','project','t','sso','alpha','photos','staff','e','auth','v2','web5','web3','mail4','devel','post','us','images2','master','rt','ftp1','qa','wp','dns4','www6','ru','student','w3','citrix','trac','doc','img2','css','mx3','adm','web4','hr','mailserver','travel','sharepoint','sport','member','bb','agenda','link','server2','vod','uk','fw','promo','vip','noc','design','temp','gate','ns7','file','ms','map','cache','painel','js','event','mailing','db1','c','auto','img1','vpn1','business','mirror','share','cdn2','site','maps','tickets','tracker','domains','club','images1','zimbra','cvs','b2b','oa','intra','zabbix','ns8','assets','main','spam','lms','social','faq','feedback','loopback','groups','m2','cas','loghost','xml','nl','research','art','munin','dev1','gis','sales','images3','report','google','idp','cisco','careers','seo','dc','lab','d','firewall','fs','eng','ann','mail01','mantis','v','affiliates','webconf','track','ticket','pm','db2','b','clients','tech','erp','monitoring','cdn1','images4','payment','origin','client','foto','domain','pt','pma','directory','cc','public','finance','ns11','test3','wordpress','corp','sslvpn','cal','mailman','book','ip','zeus','ns10','hermes','storage','free','static1','pbx','banner','mobil','kb','mail5','direct','ipfixe','wifi','development','board','ns01','st','reviews','radius','pro','atlas','links','in','oldmail','register','s4','images6','static2','id','shopping','drupal','analytics','m1','images5','images7','img3','mx01','www7','redirect','sitebuilder','smtp3','adserver','net','user','forms','outlook','press','vc','health','work','mb','mm','f','pgsql','jp','sports','preprod','g','p','mdm','ar','lync','market','dbadmin','barracuda','affiliate','mars','users','images8','biblioteca','mc','ns12','math','ntp1','web01','software','pr','jupiter','labs','linux','sc','love','fax','php','lp','tracking','thumbs','up','tw','campus','reg','digital','demo2','da','tr','otrs','web6','ns02','mailgw','education','order','piwik','banners','rs','se','venus','internal','webservices','cm','whois','sync','lb','is','code','click','w2','bugzilla','virtual','origin-www','top','customer','pub','hotel','openx','log','uat','cdn3','images0','cgi','posta','reseller','soft','movie','mba','n','r','developer','nms','ns9','webcam','construtor','ebook','ftp3','join','dashboard','bi','wpad','admin2','agent','wm','books','joomla','hotels','ezproxy','ds','sa','katalog','team','emkt','antispam','adv','mercury','flash','myadmin','sklep','newsite','law','pl','ntp2','x','srv1','mp3','archives','proxy2','ps','pic','ir','orion','srv','mt','ocs','server3','meeting','v1','delta','titan','manager','subscribe','develop','wsus','oascentral','mobi','people','galleries','wwwtest','backoffice','sg','repo','soporte','www8','eu','ead','students','hq','awstats','ec','security','school','corporate','podcast','vote','conf','magento','mx4','webservice','tour','s5','power','correio','mon','mobilemail','weather','international','prod','account','xx','pages','pgadmin','bfn2','webserver','www-test','maintenance','me','magazine','syslog','int','view','enews','ci','au','mis','dev3','pdf','mailgate','v3','ss','internet','host1','smtp01','journal','wireless','opac','w1','signup','database','demo1','br','android','career','listserv','bt','spb','cam','contacts','webtest','resources','1','life','mail6','transfer','app1','confluence','controlpanel','secure2','puppet','classifieds','tunet','edge','biz','host3','red','newmail','mx02','sb','physics','ap','epaper','sts','proxy1','ww1','stg','sd','science','star','www9','phoenix','pluto','webdav','booking','eshop','edit','panelstats','xmpp','food','cert','adfs','mail02','cat','edm','vcenter','mysql2','sun','phone','surveys','smart','system','twitter','updates','webmail1','logs','sitedefender','as','cbf1','sugar','contact','vm','ipad','traffic','dm','saturn','bo','network','ac','ns13','webdev','libguides','asp','tm','core','mms','abc','scripts','fm','sm','test4','nas','newsletters','rsc','cluster','learn','panelstatsmail','lb1','usa','apollo','pre','terminal','l','tc','movies','sh','fms','dms','z','base','jwc','gs','kvm','bfn1','card','web02','lg','editor','metrics','feed','repository','asterisk','sns','global','counter','ch','sistemas','pc','china','u','payments','ma','pics','www10','e-learning','auction','hub','sf','cbf8','forum2','ns14','app2','passport','hd','talk','ex','debian','ct','rc','2012','imap4','blog2','ce','sk','relay2','green','print','geo','multimedia','iptv','backup2','webapps','audio','ro','smtp4','pg','ldap2','backend','profile','oldwww','drive','bill','listas','orders','win','mag','apply','bounce','mta','hp','suporte','dir','pa','sys','mx0','ems','antivirus','web8','inside','play','nic','welcome','premium','exam','sub','cz','omega','boutique','pp','management','planet','ww3','orange','c1','zzb','form','ecommerce','tmp','plus','openvpn','fw1','hk','owncloud','history','clientes','srv2','img4','open','registration','mp','blackboard','fc','static3','server4','s6','ecard','dspace','dns01','md','mcp','ares','spf','kms','intranet2','accounts','webapp','ask','rd','www-dev','gw2','mall','bg','teste','ldap1','real','m3','wave','movil','portal2','kids','gw1','ra','tienda','private','po','2013','cdn4','gps','km','ent','tt','ns21','at','athena','cbf2','webmail3','mob','matrix','ns15','send','lb2','pos','2','cl','renew','admissions','am','beta2','gamma','mx5','portfolio','contest','box','mg','wwwold','neptune','mac','pms','traveler','media2','studio','sw','imp','bs','alfa','cbf4','servicedesk','wmail','video2','switch','sam','sky','ee','widget','reklama','msn','paris','tms','th','vega','trade','intern','ext','oldsite','learning','group','f1','ns22','ns20','demo3','bm','dom','pe','annuaire','portail','graphics','iris','one','robot','ams','s7','foro','gaia','vpn3']

            subdomain_store = []
            for subdoms in subdomain_array:
                try:
                    ip_value = dns.resolver.resolve(f'{subdoms}.{domain}', 'A')
                    if ip_value:
                        subdomain_store.append(f'{subdoms}.{domain}')

                except dns.resolver.NXDOMAIN:
                    pass

                except dns.resolver.NoAnswer:
                    pass 
            sub_obj.res = {"subdomain":subdomain_store}
            sub_obj.save()
        serialized_data = SubDomainSerializer(sub_obj).data
        return JsonResponse(data=serialized_data)
    


def whatcms(request):
    case_number = request.GET.get("case_number",None)
    domain = request.GET.get("domain",None)
    if case_number in ['',None]:
        base_url = 'https://whatcms.org/API/Tech?key='
        base_url1 = '&url='
        key = 'wc5teh0nb4pre63xmlazj4jq21wvvgm74wmgrnbgr2b6b8wipp43q9jj814otr6hj54qds'

        request_url = base_url+key+base_url1+domain
        response = requests.get(request_url)
        data = response.json()

        PLUGIN = []
        VERSION = []
        CATEGORIES = []

        for i in data['results']:
            PLUGIN.append(i['name'])
            if i['version'] == "":
                VERSION.append("NOT FOUND")
            else:
                VERSION.append(i['version'])
            CATEGORIES += i['categories']

        return JsonResponse({"plugin":PLUGIN,"version":VERSION,"categories":CATEGORIES})
    else:
        case_obj = Case.objects.get(case_number = case_number)
        what_obj,created = WhatCms.objects.get_or_create(case_obj=case_obj)
        if created:
            base_url = 'https://whatcms.org/API/Tech?key='
            base_url1 = '&url='
            key = 'wc5teh0nb4pre63xmlazj4jq21wvvgm74wmgrnbgr2b6b8wipp43q9jj814otr6hj54qds'

            request_url = base_url+key+base_url1+domain
            response = requests.get(request_url)
            data = response.json()

            PLUGIN = []
            VERSION = []
            CATEGORIES = []

            for i in data['results']:
                PLUGIN.append(i['name'])
                if i['version'] == "":
                    VERSION.append("NOT FOUND")
                else:
                    VERSION.append(i['version'])
                CATEGORIES += i['categories']
            what_obj.res = {"plugin":PLUGIN,"version":VERSION,"categories":CATEGORIES }
            what_obj.save()

        serialized_data = WhatCmsSerializer(what_obj).data
        return JsonResponse(data=serialized_data)









