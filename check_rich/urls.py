#coding=utf-8
'''
Created on 2016年10月28日

@author: xiaochengcao
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^check_rich/$', views.check_rich, {'template': 'check_rich/check_rich.html'}, name='check_rich'),
    url(r'^query_comment/$', views.comment, {'template': 'check_rich/comment.html'}, name='comment'),
    url(r'^add_comment/$', views.comment, {'template': 'check_rich/add_comment.html'}, name='add_comment'),
]