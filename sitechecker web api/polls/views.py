from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world!")

import requests
from bs4 import BeautifulSoup
import csv


def main(url):
    with requests.Session() as req:
        r = req.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = [item.text for item in soup.select("loc")]
        with open("./media/desss_data.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Url", "Status Code"])
            for link in links:
                r = req.get(link)
                #print(link, r.status_code)
                writer.writerow([link, r.status_code])
                soup = BeautifulSoup(r.content, 'html.parser')
                end = [item.text for item in soup.select("loc")]
                for a in end:
                    r = req.head(a)
                    #print(a, r.status_code)
                    writer.writerow([a, r.status_code])


#main("https://www.sigortam.net/sitemap.xml")
#main("https://www.desss.com/sitemap.xml")
#https://www.zoho.com/sitemap-index.xml

def csvs(request):
    documents = Document.objects.all()
    #rank = Document.objects.latest('id')
    #print(rank)
    for obj in documents:
        baseurls = obj.url
        #print(rank)
    print(baseurls)
    with requests.Session() as req:
        r = req.get(baseurls)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = [item.text for item in soup.select("loc")]
        with open("./media/desss_data.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Url", "Status Code"])
            for link in links:
                r = req.get(link)
                print(link, r.status_code)
                writer.writerow([link, r.status_code])
                soup = BeautifulSoup(r.content, 'html.parser')
                end = [item.text for item in soup.select("loc")]
                for a in end:
                    r = req.head(a)
                    print(a, r.status_code)
                    writer.writerow([a, r.status_code])
    return HttpResponse("Hello, world!")


def form_upload(request):
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

