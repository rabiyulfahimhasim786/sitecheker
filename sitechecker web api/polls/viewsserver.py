# from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from .models import Document, Sitemap, Statuscode, Expirydata
from .forms import DocumentForm, SitemapForm, StatuscodeForm, ExpirydataForm
#from .models import Document, Sitemap
#from .forms import DocumentForm, SitemapForm
import time
def index(request):
    return HttpResponse("Hello, world!")
import json
import numpy as np
import requests
# import advertools as adv
import pandas as pd
pd.options.display.max_columns = None

import csv

import csv
import re
import socket
import ssl
import datetime

def ssl_expiry_datetime(hostname):
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    context.check_hostname = False

    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 5 second timeout
    conn.settimeout(5.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)

def csvs(request):
    documents = Document.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        rank = obj.document.url
        #print(rank)
    #print(rank)
    with open('/var/www/ssl/site'+rank, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        fsa=[]
        for row in reader:
            count = count+1
            #print(row[2])
            fsa.append(row[0])
        print(fsa[1:])
    easy = []
    for x in fsa[1:]:
        try:
            response = requests.get(x)
        except Exception as e:
            #print(f"NOT OK: {str(e)}")
            a = f"NOT OK: {str(e)}"
            easy.append(a)
        else:
            if response.status_code == 200:
                #print("OK")
                a = "OK"
                easy.append(a)
            else:
                #print(f"NOT OK: HTTP response code {response.status_code}")
                a = f"NOT OK: HTTP response code {response.status_code}"
                easy.append(a)
                #print(x)
    #print(easy)
    ssl = []
    for url in fsa[1:]:
        try:
            req = requests.get(url, verify=True)
            a = url + ' has a valid SSL certificate!'
            ssl.append(a)
            #print(url + ' has a valid SSL certificate!')
        except requests.exceptions.SSLError:
            a = url + ' has INVALID SSL certificate!'
            ssl.append(a)
            #print(url + ' has INVALID SSL certificate!')
    domains_url = []
    for d in fsa[1:]:
        #print(x)
        urla = re.sub("^(https?://)?(http?://)?(www\.)?", "", d.strip('/'))
        domains_url.append(urla)
    #print(domains_url)
    espirydate = []
    for value in domains_url:
        now = datetime.datetime.now()
        try:
            expire = ssl_expiry_datetime(value)
            diff = expire - now
            print ("Domain name: {} Expiry Date: {} Expiry Day: {}".format(value,expire.strftime("%Y-%m-%d"),diff.days))
            expired = "Domain name: {} Expiry Date: {} Expiry Day: {}".format(value,expire.strftime("%Y-%m-%d"),diff.days)
            espirydate.append(expired)
        except Exception as e:
            print (e)
            expired = e
            espirydate.append(expired)
        
    dframe = pd.DataFrame({'Urls': fsa[1:],
                   'Status_code': easy,
                   'SSL': ssl,
                   'Expiry_date': espirydate,})
    # dframe = pd.DataFrame({'Urls': fsa[1:],
    #                'Status_code': easy,
    #                'SSL': ssl,})
    dframe.to_csv("/var/www/ssl/site/media/output/output1.csv", index=None)
    expiredf =pd.read_csv('/var/www/ssl/site/media/output/output1.csv')
    df_list = list(expiredf['Expiry_date'])
    foo = lambda x: pd.Series([i for i in reversed(x.split(' '))])
    rev = expiredf['Expiry_date'].apply(foo)
    print (rev)
    ds = rev.iloc[:,[6,3,0]]
    ds.to_csv("/var/www/ssl/site/media/input/data1.csv")
    file = pd.read_csv("/var/www/ssl/site/media/input/data1.csv")
    headerList = ['S.No', 'Domain Name', 'Expiry Date','Expiry Days']
    file.to_csv("/var/www/ssl/site/media/input/data2.csv", header=headerList, index=None, encoding='utf-8')
    filedata = "/var/www/ssl/site/media/input/data1.csv"
    dfjson = pd.read_csv(filedata , index_col=None, header=0)
    #geeks = df.to_html()
    json_records = dfjson.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    #status
    filepath = "/var/www/ssl/site/media/output/output1.csv"
    dfjson = pd.read_csv(filepath , index_col=None, header=0)
    #geeks = df.to_html()
    json_ssl = dfjson.reset_index().to_json(orient ='records')
    datassl = []
    datassl = json.loads(json_ssl)
    print(datassl)
    return render(request, 'csv.html', { 'documents': documents, 'd': data, 'dssl': datassl })
    #return render(request, 'csv.html', { 'documents': documents })
    # return HttpResponse("Hello, world!"+rank)

def csv_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #func_obj = form
            #func_obj.sourceFile = form.cleaned_data['sourceFile']
            form.save()
            #print(form.Document.document)
            #form.save()
            return redirect('csvs')
    else:
        form = DocumentForm()
        documents = Document.objects.all().order_by('-id')
    return render(request, 'form_upload.html', {
        'form': form, 'documents': documents
    })


def delete_document(request,id):
    if request.method == 'POST':
        document = Document.objects.get(id=id)
# if `save`=True, changes are saved to the db else only the file is deleted
        #document.delete(id=id)
        document.delete()
        return redirect('csv_upload')

import bs4
from bs4 import BeautifulSoup
def sitemap(request):
    sitemapdocuments = Sitemap.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in sitemapdocuments:
        baseurls = obj.url
        info = obj.info
        #print(rank)
    #print(baseurls)
    #print(info)
    with requests.Session() as req:
        r = req.get(baseurls)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = [item.text for item in soup.select("loc")]
        url = []
        codes = []
        for link in links:
          url.append(link)
          try:
            r = req.get(link)
          except Exception as e:
            #print(f"NOT OK: {str(e)}")
            b = f"NOT OK: {str(e)}"
            codes.append(b)
          else:
            if r.status_code == 200:
              #print("OK")
              # b = f"OK: HTTP response code {r.status_code}"
              b = f"OK: {r.status_code}"
              codes.append(b)
            else:
              #print(f"NOT OK: HTTP response code {r.status_code}")
              b = f"NOT OK: HTTP response code {r.status_code}"
              codes.append(b)
        #print(url)
        #print(codes)
        dataframestate = pd.DataFrame({'urls': url,
                   'status_code': codes,})
        #print(df.loc[0])
        #dataframestate
        dataframestate.to_csv("/var/www/ssl/site/media/input/data.csv", index=None)
    return render(request, 'sitemap.html', { 'sitemapdocuments': sitemapdocuments })


def sitemap_upload(request):
    if request.method == 'POST':
        form = SitemapForm(request.POST, request.FILES)
        if form.is_valid():
            #func_obj = form
            #func_obj.sourceFile = form.cleaned_data['sourceFile']
            form.save()
            #print(form.Document.document)
            #form.save()
            return redirect('sitemap')
    else:
        form = SitemapForm()
    return render(request, 'sitemap_upload.html', {
        'form': form
    })


def getStatuscode(url):
    try:
        r = requests.head(url,verify=False,timeout=5) # it is faster to only request the header
        return (r.status_code)

    except:
        return 'Notworking'
        #return -1


def statuscoderetrieve(request):
    sdocuments = Statuscode.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in sdocuments:
        statusrank = obj.csvfile.url
        #print(rank)
    print(statusrank)
    SLEEP = 0 # Time in seconds the script should wait between requests
    url_list = []
    url_statuscodes = []
    url_statuscodes.append(["url","status_code"]) # set the file header for output
    # with open('.'+statusrank, encoding='utf-8-sig') as csvfile:
    #     reader = csv.reader(csvfile)
    #     count = 0
    #     fsa=[]
    #     for row in reader:
    #         count = count+1
    #         #print(row[2])
    #         fsa.append(row[0])
    #     print(fsa[1:])
    # Url checks from file Input
    # use one url per line that should be checked
    #with open('urls.csv', newline='') as f:
    with open('/var/www/ssl/site'+statusrank, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            url_list.append(row[0])
    # Loop over full list
    for url in url_list:
        print(url)
        check = [url,getStatuscode(url)]
        time.sleep(SLEEP)
        url_statuscodes.append(check)

    # Save file
    with open("/var/www/ssl/site/media/dynamic/statuscode/urls_withStatusCode.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(url_statuscodes)
    filedata = "/var/www/ssl/site/media/dynamic/statuscode/urls_withStatusCode.csv"
    dfjson = pd.read_csv(filedata , index_col=None, header=0)
    #geeks = df.to_html()
    json_records = dfjson.reset_index().to_json(orient ='records')
    test = []
    test = json.loads(json_records)
    #return render(request, 'statuscode.html', { 'documents': sdocuments, 't': test })
    dataframe = pd.read_csv(filedata , index_col=None, header=0)
    options = ['100', '101', '102','103','201','202','203','204','205','206','207','208','226','300','301','302','303','304','305','306','307','308','400','401','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','421','422','423','424','425','426','428','429','431','451','500','501','502','503','504','505','506','507','508','510','511','Notworking']
    rslt_df = dataframe[dataframe['status_code'].isin(options)]
    rslt_df.to_csv("/var/www/ssl/site/media/dynamic/statuscode/filter.csv", index=False)
    filterdata = "/var/www/ssl/site/media/dynamic/statuscode/filter.csv"
    filterjson = pd.read_csv(filterdata , index_col=None, header=0)
    json_file = filterjson.reset_index().to_json(orient ='records')
    sample = []
    sample = json.loads(json_file)
    return render(request, 'statuscode.html', { 'documents': sdocuments, 't': test, 'f': sample })
    #return render(request, 'csv.html', { 'documents': documents })
    # return HttpResponse("Hello, world!"+rank)

def statuscsv_upload(request):
    if request.method == 'POST':
        form = StatuscodeForm(request.POST, request.FILES)
        if form.is_valid():
            #func_obj = form
            #func_obj.sourceFile = form.cleaned_data['sourceFile']
            form.save()
            #print(form.Document.document)
            #form.save()
            return redirect('statuscoderetrieve')
    else:
        form = StatuscodeForm()
        documents = Statuscode.objects.all().order_by('-id')
    return render(request, 'statuscsv_upload.html', {
        'form': form, 'documents': documents
    })


def statusdelete_document(request,id):
    if request.method == 'POST':
        csvfile = Statuscode.objects.get(id=id)
# if `save`=True, changes are saved to the db else only the file is deleted
        #document.delete(id=id)
        csvfile.delete()
        return redirect('statuscsv_upload')

def expirycsv(request):
    edocuments = Expirydata.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in edocuments:
        rank = obj.datafile.url
        #print(rank)
    #print(rank)
    with open('.'+rank, encoding='utf-8-sig') as datafile:
        reader1 = csv.reader(datafile)
        count = 0
        fsa=[]
        for row in reader1:
            count = count+1
            #print(row[2])
            fsa.append(row[0])
        #print(fsa[1:])
    urls1 = []
    for x in fsa[0:]:
        url = re.sub("^(https?://)?(http?://)?(www\.)?", "", x.strip('/'))
        urls1.append(url)
  
        domains_url = urls1
    print(urls1)
        
    espirydates = []
    for value in domains_url:
        now = datetime.datetime.now()
        try:
            expire = ssl_expiry_datetime(value)
            diff = expire - now
            print ("Domain name: {} Expiry Date: {} Expiry Day: {}".format(value,expire.strftime("%Y-%m-%d"),diff.days))
            expired = "Domain name: {} Expiry Date: {} Expiry Day: {}".format(value,expire.strftime("%Y-%m-%d"),diff.days)
            espirydates.append(expired)
        except Exception as e:
            print (e)
            expired = 'Expired'
            espirydates.append(expired)

    dframe = pd.DataFrame({#'Urls': fsa[1:],
                   #'Status_code': easy,
                   #'SSL': ssl,
                   'Expiry_date': espirydates,})
    dframe.to_csv("/var/www/ssl/site/media/sslexpiry/data1.csv", index=None)
    expiredf =pd.read_csv('/var/www/ssl/site/media/sslexpiry/data1.csv')
    df_list = list(expiredf['Expiry_date'])
    foo = lambda x: pd.Series([i for i in reversed(x.split(' '))])
    rev = expiredf['Expiry_date'].apply(foo)
    print (rev)
    ds = rev.iloc[:,[6,3,0]]
    ds.to_csv("/var/www/ssl/site/media/sslexpiry/data1.csv")
    files = pd.read_csv("/var/www/ssl/site/media/sslexpiry/data1.csv")
    headerList = ['S.No', 'Domain_Name', 'Expiry_Date','Expiry_Days']
    files.to_csv("/var/www/ssl/site/media/sslexpiry/data2.csv", header=headerList, index=None, encoding='utf-8')
    file2 = pd.read_csv("/var/www/ssl/site/media/sslexpiry/data2.csv")
    file2['Domain_Name'] = urls1
    file2.to_csv("/var/www/ssl/site/media/sslexpiry/output.csv", index=False, encoding='utf-8')
    fdata = "/var/www/ssl/site/media/sslexpiry/output.csv"

    file2['Expiry_Date'].replace('', np.nan, inplace=True)
    file2.dropna(subset=['Expiry_Date'], inplace=True)
    file2.to_csv("/var/www/ssl/site/media/sslexpiry/sslvalid.csv", index=False, encoding='utf-8')
    file6 = "/var/www/ssl/site/media/sslexpiry/sslvalid.csv"
    dfjson = pd.read_csv(file6 , index_col=None, header=0)
    json_records = dfjson.reset_index().to_json(orient ='records')
    test1 = []
    test1 = json.loads(json_records)
    

    #return render(request, 'statuscode.html', { 'documents': sdocuments, 't': test })
    dataframe = pd.read_csv(fdata , index_col=None, header=0)
    options = ['Expired']
    rslt_df = dataframe[dataframe['Expiry_Days'].isin(options)]
    rslt_df.to_csv("/var/www/ssl/site/media/sslexpiry/sslinvalid.csv", index=False)
    filterdata1 = "/var/www/ssl/site/media/sslexpiry/sslinvalid.csv"
    filterjson1 = pd.read_csv(filterdata1 , index_col=None, header=0)
    json_file = filterjson1.reset_index().to_json(orient ='records')
    sample1 = []
    sample1 = json.loads(json_file)
    return render(request, 'expiry.html', { 'Expirydata': Expirydata, 'p': test1, 'h': sample1})

def expiry_upload(request):
    if request.method == 'POST':
        form = ExpirydataForm(request.POST, request.FILES)
        if form.is_valid():
            #func_obj = form
            #func_obj.sourceFile = form.cleaned_data['sourceFile']
            form.save()
            #print(form.Document.document)
            #form.save()
            return redirect('expirycsv')
    else:
        form = ExpirydataForm()
        documents1 = Expirydata.objects.all().order_by('-id')
    return render(request, 'expiry_upload.html', {
        'form': form, 'documents1': documents1
    })

def expirydelete_document(request,id):
    if request.method == 'POST':
        datafile = Expirydata.objects.get(id=id)
# if `save`=True, changes are saved to the db else only the file is deleted
        #document.delete(id=id)
        datafile.delete()
        return redirect('expiry_upload')