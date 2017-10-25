from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MainSDKUsergameorder(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    amount = models.CharField(max_length=128)
    trade_id = models.CharField(max_length=128)
    game_order_id = models.CharField(max_length=128)
    created_at = models.CharField(max_length=128)
    updated_at = models.CharField(max_length=128)
    pay_channel = models.CharField(max_length=128)
    good_name = models.CharField(max_length=128)
    order_status = models.CharField(max_length=128)
    app_id = models.CharField(max_length=128)
    user_id = models.CharField(max_length=128)
    currency = models.CharField(max_length=128)
    real_amount = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'api_usergameorder'

class MainSDKUser(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    phone = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'api_user'

class UdbUorder(models.Model):
    orderID = models.CharField(max_length=128, primary_key=True)
    username = models.CharField(max_length=128)
    roleID = models.CharField(max_length=128)
    roleName = models.CharField(max_length=128)
    serverName = models.CharField(max_length=128)
    createdTime = models.CharField(max_length=128)
    completeTime = models.CharField(max_length=128)
    productName = models.CharField(max_length=128)
    productID = models.CharField(max_length=128)
    productDesc = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    money = models.CharField(max_length=128)
    realMoney = models.CharField(max_length=128)
    userID = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'uorder'

class UdbUuser(models.Model):
    channelUserID = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    id = models.CharField(max_length=128, primary_key=True)
    
    class Meta:
        db_table = 'uuser'