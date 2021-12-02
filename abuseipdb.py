import requests
import time
import re
from requests import ConnectionError
from urllib3.connectionpool import SocketError, SSLError, MaxRetryError, ProxyError,Timeout


def abuseipdb_threat(dns):
    url = "https://www.abuseipdb.com/whois/{dns}".format(dns=dns)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': url,
    }
    try:
        response = requests.get(url,headers=headers,timeout=10)
        status = response.status_code
    except Exception as e:
        print("Exception error")
        time.sleep(30)

    except (ConnectionError, SocketError, SSLError, MaxRetryError, ProxyError, Timeout):
        print("SSLError error")
        time.sleep(30)


    if status == 200:
        data = response.text
        dns_ = list(set(re.findall('<li>(.*)<\/li>', data)))
        _temp=[]
        for i in dns_:
            if not ("href=" or "src=" or "Prohibited") in i:
                _temp.append(i + "." + dns)

        return _temp


