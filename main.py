import abuseipdb
import crtsh
import virustotal
import time
import socket
import sys


def main(domain):
    abuse_list = abuseipdb.abuseipdb_threat(domain)
    crt_list = crtsh.crtsh(domain)

    vt = virustotal.DnsInit(dns=domain)
    prefix = vt.getPrefix()
    print("ASN : " + prefix)

    vt.nmap_up(range=prefix)
    nmap_result = vt.get_records()

    for _nmap in nmap_result:
        for ip in _nmap:
            #print(str(ip))
            vt.getSelenium(ip)
            time.sleep(6)

    vt_list = vt.get_subdomain()


    all_list = vt_list + abuse_list + crt_list
    all_list = list(dict.fromkeys(all_list))
    for i in all_list:
        ip = get_ips_by_dns_lookup(target=i)
        if ip:
            print(i, end=" - ")
            print(','.join(map(str, ip)))
        else:
            print(i)
    exit(0)





if __name__ == '__main__':

    def get_ips_by_dns_lookup(target, port=None):
        if not port:
            port = 443
        try:
            return list(map(lambda x: x[4][0], socket.getaddrinfo('{}.'.format(target), port, type=socket.SOCK_STREAM)))
        except Exception:
            return None


    argumentList = sys.argv[1:]
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("missing arg")

    exit()


