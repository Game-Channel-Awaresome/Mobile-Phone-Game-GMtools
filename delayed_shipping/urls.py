#coding=utf-8
'''
Created on 2016年10月28日

@author: xiaochengcao
'''
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^delayed_shipping/$', views.delayed_shipping, {'template': 'delayed_shipping/delayed_shipping.html'}, name='delayed_shipping'),
]