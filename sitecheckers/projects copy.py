#pip install requests
import pandas as pd
import requests
df= pd.read_csv('test.csv')
check =[]
for url in df['urls']:
    try:
        req = requests.get(url, verify=True)
        state = url + ' has a valid SSL certificate!'
        #print(url + ' has a valid SSL certificate!')
    except requests.exceptions.SSLError:
        #print(url + ' has INVALID SSL certificate!')
        state = url + ' has INVALID SSL certificate!'
    #print(state)
    #df['ssl'] = state
    check.append(state)
#print(check)
df['ssl'] = check
df.to_csv('SSL.csv')