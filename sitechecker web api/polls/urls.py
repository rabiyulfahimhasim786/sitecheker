from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('uploads/', views.simple_upload, name='simple_upload'),
    # path('formupload/', views.model_form_upload, name='model_form_upload'),
    # path('fileuploading/', views.uploadings, name='uploadings'),
    path('csvform/', views.csv_upload, name='csv_upload'),
    path('csv/', views.csvs, name='csvs'),
    path('csv/<int:id>/',views.delete_document,name='delete_document'),
    path('sitemapurl/', views.sitemap_upload, name='sitemap_upload'),
    path('sitemapxml/', views.sitemap, name='sitemap'),
    path('statusform/', views.statuscsv_upload, name='statuscsv_upload'),
    path('status/', views.statuscoderetrieve, name='statuscoderetrieve'),
    path('status/<int:id>/',views.statusdelete_document,name='statusdelete_document'),
]