import requests

def url_ok(url):
    r = requests.get(url, verify=False, timeout=5)
    print(r.status_code)
    return r.status_code == 200

url_ok('http://doctorchatbot.zunamelt.com/')