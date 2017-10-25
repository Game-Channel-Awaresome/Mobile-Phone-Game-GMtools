# coding=utf-8
import json
import time
import urlparse
import uuid
import urllib, urllib2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from forms import DelayedShippingForm

from models import MainSDKApp, MainSDKUser, ApiToolsShippingHistory2, U8Uorder
from utils.__init__ import get_signature


@login_required(login_url='/admin/login/')
def delayed_shipping(request, template):
    apitoolsusername = ':' + request.user.username
    appname_id = MainSDKApp.objects.using('apiserver_db').all()
    if request.method == 'GET':
        form = DelayedShippingForm()
        return render(request, template, {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                          'guestlist': settings.GUEST})
    elif request.method == 'POST':
        if apitoolsusername in settings.GUEST:
            form = DelayedShippingForm(request.POST)
            return render(request, template, {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                              'guestlist': settings.GUEST})
        form = DelayedShippingForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['captcha'].lower() != request.session['captcha']:
                form.add_error('captcha', '验证码错误')
            else:
                appid = cleaned_data['appid']
                orderid = cleaned_data['orderid']
                price = cleaned_data['price'] * 100
                productid = cleaned_data['productid']
                try:
                    app = MainSDKApp.objects.using('apiserver_db').get(appid=appid)
                except MainSDKApp.DoesNotExist:
                    form.add_error('appid', 'appid在SDK服务器中不存在')
                else:
                    try:
                        U8Uorder.objects.using('u8server_db').get(orderId=orderid)
                    except Exception:
                        form.add_error('orderid', 'U8服务器上不存在此订单')
                        return render(request, template,
                                      {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                       'guestlist': settings.GUEST})
                    pay_callback_url = app.pay_callback_url
                    parsed_u8_callback_url = urlparse.urlparse(pay_callback_url)
                    user = MainSDKUser.objects.using('apiserver_db').get(username='innerbudanuser')
                    request_args = [('AppOrderID', orderid), ('Price', price), ('Uid', user.id),
                                    ('ChannelOrderID', uuid.uuid4().get_hex()), ('ProductID', productid)]
                    request_query_str = '&'.join(['='.join(map(str, item)) for item in request_args])
                    new_u8_parsed_callback_url = urlparse.ParseResult(scheme=parsed_u8_callback_url.scheme,
                                                                      netloc=parsed_u8_callback_url.netloc,
                                                                      path=parsed_u8_callback_url.path,
                                                                      params=parsed_u8_callback_url.params,
                                                                      query=request_query_str,
                                                                      fragment=parsed_u8_callback_url.fragment)
                    new_u8_callback_url = urlparse.urlunparse(new_u8_parsed_callback_url)
                    callback_sign = get_signature(app.appsecret.encode('utf-8'), new_u8_callback_url)
                    request_args.append(('sign', callback_sign))
                    request_args_map = dict(request_args)
                    request_obj = urllib2.Request(pay_callback_url)
                    request_obj.add_data(urllib.urlencode(request_args_map))
                    try:
                        response = urllib2.urlopen(request_obj, timeout=6).read()
                        messages.info(request, 'U8 said: %s' % response)
                    except Exception as e:
                        messages.error(request, 'Exception: %s' % str(e))
                    else:
                        if json.loads(response)['status'] == 'success':
                            infostr = '订单发货成功'
                            try:
                                ApiToolsShippingHistory2.objects.using('default').create(username=apitoolsusername[1:],
                                                                                         time=time.strftime(
                                                                                             '%Y-%m-%d %H:%M:%S',
                                                                                             time.localtime(
                                                                                                 time.time() + 28800)),
                                                                                         orderid=orderid, price=price,
                                                                                         appid=appid)
                            except Exception:
                                infostr = infostr + ',写入缓存失败'
                            messages.success(request, infostr)
                        else:
                            messages.error(request, '修改U8服务器失败')
        return render(request, template, {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                          'guestlist': settings.GUEST})
