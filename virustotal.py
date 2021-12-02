from cymruwhois import Client
import socket
import nmap
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
import threading
import asyncio
import re
from libselenium import *



class DnsInit(object):
    """"""
    subdomains=[]
    def __init__(self, dns=None):
        """"""
        self.domain = dns
        self.nmap_result = None

    def getPrefix(self):
        c = Client()
        ip = socket.gethostbyname(self.domain)
        prefix = c.lookup(ip).prefix
        return prefix

    def nmap_up(self, range):
        nm = nmap.PortScanner()
        up_host = nm.scan(hosts=range, arguments='-sn')
        self.nmap_result = up_host
        return up_host

    def get_records(self):
        records = []
        if not self.nmap_result is None:
            scaninfo = self.nmap_result["scan"]
            for ip in scaninfo:
                name = scaninfo[ip]["hostnames"][0]["name"]
                records.append({ip:name})
        return records

    def getSelenium(self, ip):
        browser.get('https://www.virustotal.com/gui/ip-address/{ip}/relations'.format(ip=ip))

    def next_Selenium(self, url):
        browser.get(url)

    def get_subdomain(self):
        self.subdomains = list(dict.fromkeys(self.subdomains))
        return self.subdomains

    def request(self, flow):
        pass

    def response(self, flow):
        #print(flow.request.path)
        #x = flow.response.get_text()
        if "/ui/ip_addresses/" in flow.request.path and "/resolutions" in flow.request.path:
            response = flow.response.get_text()
            dns_list = list(set(re.findall(r'"host_name":\W"(.*)"', response)))
            self.subdomains += dns_list
            #print(str(len(self.subdomains)))
            #print(dns_list)
            #print(flow.response.get_text())
            #response = response.replace('\n', '')
            #response = json.loads(response)
            #nextLink = response["links"]["next"]
            #self.next_Selenium(nextLink)



def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


mitmoptions = Options(listen_host='0.0.0.0', listen_port=8080, http2=True)
m = DumpMaster(mitmoptions, with_termlog=False, with_dumper=False)
config = ProxyConfig(mitmoptions)
m.server = ProxyServer(config)
m.addons.add(DnsInit())
loop = asyncio.get_event_loop()
t = threading.Thread(target=loop_in_thread, args=(loop, m))
t.start()


def killmitm():
    m.shutdown()


