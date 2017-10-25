#coding=utf-8
'''
Created on 2016年10月28日

@author: xiaochengcao
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^check_order/$', views.check_order, {'template': 'check_order/check_order.html'}, name='check_order'),
]