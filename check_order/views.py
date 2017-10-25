#coding=utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from forms import CheckOrderForm

from models import MainSDKUsergameorder, UdbUorder, UdbUuser, MainSDKUser

@login_required(login_url='/admin/login/')
def check_order(request, template):
    apitoolsusername = ':'+request.user.username
    if request.method == 'GET':
        form = CheckOrderForm()
        return render(request, template, {'form': form, 'username': apitoolsusername})
    elif request.method == 'POST':
        form = CheckOrderForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            userid = cleaned_data['userid']
            orderid = cleaned_data['orderid']
            if request.POST.has_key("byorderid"):
                if orderid == '' or orderid == None:
                    form.add_error('orderid', '请填写此字段')
                else:
                    sdkresult = MainSDKUsergameorder.objects.using('apiserver_db').filter(game_order_id = orderid)
                    u8result = UdbUorder.objects.using('u8server_db').filter(orderID = orderid)
                    if len(sdkresult) == 0 and len(u8result) == 0 :
                        form.add_error('orderid', '服务器中无此OrderID的记录')
                    elif len(sdkresult) == 0:
                        form.add_error('orderid', 'OrderID在SDK服务器中不存在，只显示U8服务器查询结果')
                    elif len(u8result) == 0:
                        sdkuser = MainSDKUser.objects.using('apiserver_db').get(id = MainSDKUsergameorder.objects.using('apiserver_db').get(game_order_id = orderid).user_id)
                        form.add_error('orderid', 'OrderID在U8服务器中不存在，只显示SDK服务器查询结果')
                        return render(request, template, {'form': form, 'sdkresult': sdkresult, 'u8result': u8result, 'username': apitoolsusername, 'sdkuser': sdkuser})
                    else:
                        sdkuser = MainSDKUser.objects.using('apiserver_db').get(id = MainSDKUsergameorder.objects.using('apiserver_db').get(game_order_id = orderid).user_id)
                        messages.success(request, '查询成功')
                        return render(request, template, {'form': form, 'sdkresult': sdkresult, 'u8result': u8result, 'username': apitoolsusername, 'sdkuser': sdkuser})
                    return render(request, template, {'form': form, 'sdkresult': sdkresult, 'u8result': u8result, 'username': apitoolsusername})
            elif request.POST.has_key("byuserid"):
                if userid == '' or userid == None:
                    form.add_error('userid', '请填写此字段')
                else:
                    try:
                        u8user = UdbUuser.objects.using('u8server_db').get(name = userid)
                    except Exception:
                        form.add_error('userid', '此用户在U8服务器中不存在')
                        return render(request, template, {'form': form, 'username': apitoolsusername})
                    try:
                        sdkuser = MainSDKUser.objects.using('apiserver_db').get(id = u8user.channelUserID)
                    except Exception:
                        form.add_error('userid', '此用户在SDK服务器中不存在')
                        sdkresult = ''
                        sdkuser = ''
                    else:
                        sdkresult = MainSDKUsergameorder.objects.using('apiserver_db').filter(user_id = sdkuser.id)
                    u8result = UdbUorder.objects.using('u8server_db').filter(username = userid)
                    if len(sdkresult) == 0 and len(u8result) == 0:
                        form.add_error('userid', '此用户并没有订单信息，只显示用户信息')
                    elif len(sdkresult) == 0:
                        form.add_error('userid', 'SDK服务器上无此用户的订单信息，只显示U8查询结果')
                    elif len(u8result) == 0:
                        form.add_error('userid', 'U8服务器上无此用户的订单信息，只显示SDK查询结果')
                    return render(request, template, {'form': form, 'sdkresult': sdkresult, 'u8result': u8result, 'username': apitoolsusername, 'sdkuser': sdkuser})
        return render(request, template, {'form': form, 'username': apitoolsusername})