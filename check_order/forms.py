#coding=utf-8
'''
Created on Oct 27, 2016

@author: Felix
'''
from django import forms

class CheckOrderForm(forms.Form):
    '''Delayed Shipping Form'''
    userid = forms.CharField(required=False, 
                               widget=forms.TextInput(attrs={'id': 'userid', 'placeholder': '请输入用户ID(例如 1234567890.ios.heyijoy)', 'class': 'form-control'}))
    orderid = forms.CharField(required=False, 
                              max_length=64, 
                              widget=forms.TextInput(attrs={'id': 'orderid', 'placeholder': '请输入订单号(U8)', 'class': 'form-control'}))
