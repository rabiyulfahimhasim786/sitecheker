# from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse

from .models import Document, Sitemap
from .forms import DocumentForm, SitemapForm
def index(request):
    return HttpResponse("Hello, world!")

import requests
# import advertools as adv
import pandas as pd
pd.options.display.max_columns = None

import csv
    
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
        
    dframe = pd.DataFrame({'Urls': fsa[1:],
                   'Status_code': easy,
                   'SSL': ssl,})
    dframe.to_csv("/var/www/ssl/site/media/output/output1.csv", index=None)
    return render(request, 'csv.html', { 'documents': documents })
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
    return render(request, 'form_upload.html', {
        'form': form
    })
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
        dataframestate.to_csv("/var/www/ssl/site/media/input/output.csv", index=None)
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
