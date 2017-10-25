#coding=utf-8
'''
Created on Oct 27, 2016

@author: Felix
'''
from django import forms
from models import MainSDKApp

class DelayedShippingForm(forms.Form):
    '''Delayed Shipping Form'''
    appid = forms.ChoiceField(required=True, choices=((appname_id.appid,appname_id.name) for appname_id in MainSDKApp.objects.using('apiserver_db').all()),
                              widget=forms.Select(attrs={'class':'form-control'}), initial='3')
    orderid = forms.CharField(required=True, 
                              max_length=64, 
                              widget=forms.TextInput(attrs={'id': 'orderid', 'placeholder': '请输入订单号(U8)', 'class': 'form-control', 'required': 'true'}))
    productid = forms.CharField(required=True, 
                              max_length=64, 
                              widget=forms.TextInput(attrs={'id': 'productid', 'placeholder': '例如:com.shouxuezairan_cny_gold_6', 'class': 'form-control', 'required': 'true'}))
    price = forms.IntegerField(required=True, 
                               widget=forms.TextInput(attrs={'id': 'price', 'placeholder': '请输入订单金额（以元为单位）', 'class': 'form-control', 'required': 'true'}))
    captcha = forms.CharField(required=True, 
                              max_length=4,
                               widget=forms.TextInput(attrs={'id': 'captcha', 'placeholder': '请输入验证码(不区分大小写)', 'class': 'form-control', 'required': 'true'}))    
