from django import forms
from .models import Document, Sitemap, Statuscode, Expirydata

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )


class SitemapForm(forms.ModelForm):
    class Meta:
        model = Sitemap
        fields = ('url', 'info',)

class StatuscodeForm(forms.ModelForm):
    class Meta:
        model = Statuscode
        fields = ('name', 'csvfile', )

class ExpirydataForm(forms.ModelForm):
    class Meta:
        model = Expirydata
        fields = ('title', 'datafile', )