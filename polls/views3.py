# from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse

from .models import Document, Sitemap
from .forms import DocumentForm, SitemapForm
def index(request):
    return HttpResponse("Hello, world!")
import json
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
        documents = Document.objects.all()
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
