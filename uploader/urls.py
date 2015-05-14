__author__ = 'alex'
from django.conf.urls import patterns, url
from .views import ImageCreateView
urlpatterns = [
    url(r'^new/$', ImageCreateView.as_view(), name='upload-new'),
]