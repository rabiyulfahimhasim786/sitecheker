from django.db import models
# Create your models here.
from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete()
            super().delete(*args, **kwargs)

class Sitemap(models.Model):
    info = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Statuscode(models.Model):
    name = models.CharField(max_length=255, blank=True)
    csvfile = models.FileField(upload_to='dynamic/')
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.csvfile:
            self.csvfile.delete()
            super().delete(*args, **kwargs)