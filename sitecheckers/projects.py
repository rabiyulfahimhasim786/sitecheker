#pip install requests
import pandas as pd
import requests
df= pd.read_csv('test.csv')
for url in df['urls']:
    response= requests.get(url)
    status= response.status_code
    df['Status']=status


df.to_csv('Status_codes.csv')