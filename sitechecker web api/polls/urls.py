from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_upload, name='form_upload'),
    path('csv/', views.csvs, name='csvs'),
]