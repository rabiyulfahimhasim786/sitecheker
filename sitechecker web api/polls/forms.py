from django import forms
from .models import Document, Sitemap

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )


class SitemapForm(forms.ModelForm):
    class Meta:
        model = Sitemap
        fields = ('url', 'info',)