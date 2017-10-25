#coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MainSDKApp(models.Model):
    appid = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=128, default='')
    pay_callback_url = models.URLField(verbose_name='支付回调地址', default='', max_length=256)
    appsecret = models.CharField(verbose_name="App Secret Key", max_length=128, default='')
    
    class Meta:
        db_table = 'api_app'

class MainSDKUser(models.Model):
    id = models.CharField(verbose_name="User ID", max_length=128, primary_key=True)
    username = models.CharField(verbose_name="User Name", max_length=128, unique=True, null=True, db_index=True)
    
    class Meta:
        db_table = 'api_user'
        
class ApiToolsShippingHistory2(models.Model):
    orderid = models.CharField(max_length=128, null=False, primary_key=True)
    appid = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    time = models.CharField(max_length=128, null=False)
    username = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'shipping_history2'
    
class U8Uorder(models.Model):
    orderId = models.IntegerField(null=False, primary_key=True)
    productID = models.CharField(null=False, default='', max_length=128)
    class Meta:
        db_table = 'uorder'