import urllib2
import socket

def check_url( url, timeout=5 ):
    try:
        return urllib2.urlopen(url,timeout=timeout).getcode() == 200
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:
        print(False)


print(check_url("http://google.fr"))  #True 
print(check_url("http://notexist.kc")) #False     
