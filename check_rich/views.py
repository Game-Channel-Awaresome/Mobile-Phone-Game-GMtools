# coding=utf-8
import time
import json
import hashlib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.cache import cache
from excel_response3 import ExcelResponse

from forms import CheckRichForm, CommentForm, SearchForm
from models import UdbUorder, UdbUuser, MainSDKUser, MainSDKApp, Comment
# Create your views here.
from django.conf import settings


@login_required(login_url='/admin/login/')
def check_rich(request, template):
    apitoolsusername = ':' + request.user.username
    appname_id = MainSDKApp.objects.using('apiserver_db').all()
    if request.method == 'GET' and not request.GET.has_key('export'):
        form = CheckRichForm()
        return render(request, template, {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                          'guestlist': settings.GUEST})
    elif request.method == 'POST':
        if apitoolsusername in settings.GUEST:
            form = CheckRichForm(request.POST)
            return render(request, template, {'form': form, 'username': apitoolsusername, 'appname_id': appname_id,
                                              'guestlist': settings.GUEST})
        form = CheckRichForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['captcha'].lower() != request.session['captcha']:
                form.add_error('captcha', '验证码错误')
            else:
                result = {}
                appid = cleaned_data['appid']
                starttime = cleaned_data['starttime']
                endtime = cleaned_data['endtime']
                price = cleaned_data['price'] * 100
                if not starttime:
                    starttime = 0
                else:
                    starttime = int(starttime)
                if not endtime:
                    endtime = 99991231
                else:
                    endtime = int(endtime)
                u8orders = UdbUorder.objects.using('u8server_db').raw(
                    'select b.userID, b.username as orderID,b.pricesum from (select a.username, a.userID, sum(a.realMoney) as pricesum from (select * from uorder where appID=%s and state=3 and completeTime between %s and %s and username like \'%%heyijoy%%\')a group by a.username)b where b.pricesum>%s',
                    [appid, starttime, endtime, price])
                if len(u8orders.params) == 0:
                    form.add_error('price', '没有符合要求的记录')
                    return render(request, template,
                                  {'form': form, 'username': apitoolsusername, 'rich_num': 0, 'appname_id': appname_id,
                                   'guestlist': settings.GUEST})
                for u8order in u8orders:
                    result[u8order.orderID] = {}
                    result[u8order.orderID]['price'] = str(u8order.pricesum / 100)
                    result[u8order.orderID]['user_id'] = u8order.userID
                    eachrich_orders = UdbUorder.objects.using('u8server_db').filter(username=u8order.orderID)
                    distanct_roleid = set([])
                    result[u8order.orderID]['roleandserver'] = []
                    for eachorder in eachrich_orders:
                        setlen = len(distanct_roleid)
                        if eachorder.state == 3:
                            distanct_roleid.add(eachorder.roleID)
                        if len(distanct_roleid) != setlen:
                            roles = UdbUorder.objects.using('u8server_db').filter(roleID=eachorder.roleID)
                            role_haspay = 0
                            for role in roles:
                                if role.realMoney and role.state == 3:
                                    role_haspay = role_haspay + role.realMoney
                            result[u8order.orderID]['roleandserver'].append(
                                [eachorder.roleID, eachorder.roleName, eachorder.serverID, eachorder.serverName,
                                 role_haspay / 100])
                    U8richuser = UdbUuser.objects.using('u8server_db').get(name=u8order.orderID)
                    channelUserID = U8richuser.channelUserID
                    if U8richuser.lastLoginTime:
                        result[u8order.orderID]['lastlogin'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                            float(U8richuser.lastLoginTime) / 1000))
                    result[u8order.orderID]['channelUserID'] = str(channelUserID)
                    try:
                        sdkrich = MainSDKUser.objects.using('apiserver_db').get(id=channelUserID)
                    except Exception:
                        pass
                    else:
                        result[u8order.orderID]['phone'] = sdkrich.phone
                        result[u8order.orderID]['signname'] = sdkrich.username
                rich_num = len(result)
                temp_key = str(price) + str(appid) + str(starttime) + str(endtime)
                redis_key = hashlib.md5(temp_key).hexdigest()
                cache.set(redis_key, json.dumps(result), 1800)
                return render(request, template,
                              {'form': form, 'username': apitoolsusername, 'rich_num': rich_num, 'result': result,
                               'appname_id': appname_id, 'guestlist': settings.GUEST, 'redis_key':redis_key})
    else:
        excel_result = []
        values = []
        keys = [u"user_id", u"channelUserID", u"price", u"lastlogin", u"signname", u"phone", u"roleandserver"]
        headers = [u"用户ID", u"用户渠道ID", u"总支付金额（元）", u"最近登录时间", u"登录名", u"手机号", u"角色ID", u"角色名", u"服务器ID",
                   u"服务器名", u"充值金额（元）"]
        key_arg = request.GET['export']
        try:
            redis_temp = cache.get(key_arg)
            assert type(redis_temp) == type("")
        except AssertionError:
            return render(request, "check_rich/error.html")
        for username, value in json.loads(redis_temp).items():
            value["user_id"] = username
            values.append(value)
        for i in values:
            temp = []
            for key in keys:
                temp.append(i.get(key, ""))
            excel_result.append(temp)
        new_excel = []
        for i in excel_result:
            temp = i.pop()
            for j in temp:
                new_excel.append(i + j)
        new_excel.insert(0, headers)
        return ExcelResponse(new_excel)
    return render(request, template,
                  {'form': form, 'username': apitoolsusername, 'appname_id': appname_id, 'guestlist': settings.GUEST})


@login_required(login_url='/admin/login/')
def comment(request, template):
    apitoolsusername = ':' + request.user.username
    player_name = request.GET.get('player_name')
    userid = request.user.id
    userid_instance = User.objects.using('default').get(id=userid)
    username = apitoolsusername
    guestlist = settings.GUEST
    search_form = SearchForm()
    if request.method == 'GET':
        form = CommentForm()
        comment_result = Comment.objects.using('default').filter(player_name=player_name)
        comment_num = len(comment_result)
        return render(request, template, locals())
    elif request.method == 'POST' and request.POST.has_key('keyword'):
        keyword = request.POST.get('keyword')
        search_form=SearchForm(initial={'keyword':keyword})
        comment_result = Comment.objects.using('default').filter(player_name=player_name, comment_content__contains= keyword)
        comment_num = len(comment_result)
        return render(request, template, locals())
    elif request.method == "POST":
        if apitoolsusername in settings.GUEST:
            form = CommentForm(request.POST)
            return render(request, template, locals())
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = cleaned_data['add_comment']
            # try:
            Comment.objects.using('default').create(comment_content= comment,
                                                    comment_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() + 28800)),
                                                    player_name=player_name,
                                                    user = userid_instance
                                                    )
            # except Exception:
            #     raise IOError

            return render(request, "check_rich/success.html", locals())

        # return render(request,template)
