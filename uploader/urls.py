__author__ = 'alex'
from django.conf.urls import patterns, url
from .views import ImageCreateView, ImageDeleteView, ImageListView
urlpatterns = [
    url(r'^new/$', ImageCreateView.as_view(), name='upload_new'), #главна страница
    url(r'^list/$', ImageListView.as_view(), name='upload_list'), #список загруженных файлов
    url(r'^delete/(?P<pk>\d+)$', ImageDeleteView.as_view(), name='upload_delete'),#удалить файл с ключом pk
]