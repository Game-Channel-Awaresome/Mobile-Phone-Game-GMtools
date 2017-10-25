# coding=utf-8
'''
Created on Oct 27, 2016

@author: Felix
'''
from django import forms
from models import MainSDKApp


class CheckRichForm(forms.Form):
    '''Delayed Shipping Form'''
    appid = forms.ChoiceField(required=True, choices=((appname_id.appid, appname_id.name) for appname_id in
                                                      MainSDKApp.objects.using('apiserver_db').all()),
                              widget=forms.Select(attrs={'class': 'form-control'}), initial='3')
    price = forms.IntegerField(required=True,
                               widget=forms.TextInput(
                                   attrs={'id': 'price', 'placeholder': '请输入查询金额(以元为单位)', 'class': 'form-control',
                                          'required': 'true'}))
    starttime = forms.CharField(required=False,
                                max_length=8,
                                widget=forms.TextInput(
                                    attrs={'id': 'starttime', 'placeholder': '请输入查询的起始日期(含),如20161103',
                                           'class': 'form-control'}))
    endtime = forms.CharField(required=False,
                              max_length=8,
                              widget=forms.TextInput(attrs={'id': 'endtime', 'placeholder': '请输入查询的截止日期(不含),如20161107',
                                                            'class': 'form-control'}))
    captcha = forms.CharField(required=True,
                              max_length=4,
                              widget=forms.TextInput(
                                  attrs={'id': 'captcha', 'placeholder': '请输入验证码(不区分大小写)', 'class': 'form-control',
                                         'required': 'true'}))


class CommentForm(forms.Form):
    """comment Form"""
    add_comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '请输入备注内容', 'class': 'form-control'}))



class SearchForm(forms.Form):
    """search Form"""
    keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '请输入要搜索的备注内容', 'class': 'form-control'}))



