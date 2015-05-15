__author__ = 'alex'
from django.conf.urls import patterns, url
from .views import ImageCreateView, ImageDeleteView
urlpatterns = [
    url(r'^new/$', ImageCreateView.as_view(), name='upload_new'),
    url(r'^delete/(?P<pk>\d+)$', ImageDeleteView.as_view(), name='upload_delete'),
]