import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from index.forms import *

# Create your views here.


def index_views(request):
    return render(request,'index.html')

def login_views(request):
    if request.method == 'GET':
        # 获取请求源地址,如果没有的话则获取'/'
        url = request.META.get('HTTP_REFERER','/')


        # print("请求源地址:"+url)
        # 判断uid和uphoned的值是否在session中
        if 'uid' in request.session and 'uphone' in request.session:
            # 如果存在返回首页
            return redirect(url)
        else:
            # 判断cookies中是否有uid和uphone,如果有取出来保存进session,再回首页
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid']=uid
                request.session['uphone']=uphone
                return redirect(url)
            # 否则去往登录页
            else:
                form = LoginForm()
                # 将url保存进cookies,以便提供给post去使用
                # 先构建响应对象,然后再将cookies保存进响应对象中
                resp = render(request,'login.html',locals())
                resp.set_cookie('url', url)
                return resp

    else:
        # 获取请求源地址
        url = request.META.get('HTTP_REFERER','/')
        # print("POST中的请求源地址:"+url)
        # 接收前端数据,判断登录
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']

        users = Users.objects.filter(uphone=uphone,upwd=upwd)
        if users:
            # 登录成功,将id和uphone保存进session
            id=users[0].id
            request.session['uid']=id
            request.session['uphone']=uphone
            # 如果记住密码,保存进cookies
            # 先从cookies中将URL的值获取出来
            url = request.COOKIES.get('url','/')
            resp = redirect(url)
            # 如果url存在于cookies中,则将url从cookies中删除出去
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            if 'isSave' in request.POST:
                expires = 60*60*24*365
                resp.set_cookie('uid',id,expires)
                resp.set_cookie('uphone',uphone,expires)
            return resp

        else:
            # 登录失败,回到登录页面
            return redirect('/login/')


def register_views(request):
    return render(request,'register.html')


def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        # 有登录信息
        id = request.session.get('uid')
        uname = Users.objects.get(id=id).uname
        dic = {
            'loginStatus':1,
            'uname':uname,
        }
    elif 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        # cookies中有登录信息,那么从cookies中取出数据在保存进session
        uid = request.COOKIES['uid']
        uphone = request.COOKIES['uphone']
        request.session['uid'] = uid
        request.session['uphone'] = uphone
        # 根据uid的值获取对应的uname,并构建成字典再响应给客户端
        uname = Users.objects.get(id=uid).uname
        dic = {
            'loginStatus': 1,
            'uname': uname,
        }

    else:
        # 没有登录信息
        dic = {
            'loginStatus':0
        }
    return HttpResponse(json.dumps(dic))


def logout_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
        # 获取源地址
        url = request.META.get('HTTP_REFERER','/')
        resp = redirect(url)
        # 判断cookies,有则清除
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('uid')
            resp.delete_cookie('uphone')
        return resp
    return redirect('/')


def check_uphone_views(request):
    uphone = request.GET['uphone']
    users = Users.objects.filter(uphone=uphone)
    if users:
        dic = {
            'status':1,
            'msg':'手机号码已存在'
        }
    else:
        dic = {
            'status':0,
            'msg':'通过',
        }
    return HttpResponse(json.dumps(dic))


def load_type_goods(request):
    all_list = []
    # 读取GoodsType下的所有内容
    types = GoodsType.objects.all()
    for type in types:
        # 将类型转换为json的字符串
        type_json = json.dumps(type.to_dict())
        # 通过type来获取对应的商品
        goods = type.goods_set.all()[0:10]
        # 将goods转换为json的字符串
        goods_json = serializers.serialize('json',goods)
        dic = {
            'type':type_json,
            'goods':goods_json,
        }
        # 将dic追加进all_list中
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))






