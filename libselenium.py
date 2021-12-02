from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


PROXY = "127.0.0.1:8080"
webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False,
    "socks_remote_dns":False,
}
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36"')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--log-level=3")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(executable_path=r"/Users/fsirin/PycharmProjects/dnsenum/chromedriver",chrome_options=options)
