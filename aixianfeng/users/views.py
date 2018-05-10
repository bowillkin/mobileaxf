import random
import time

import datetime
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets

from users.models import MainWheel, MainShop, MainNav, MainMustBuy, MainShow, FoodType, Goods, UserModel, OrderModel, \
    OrderGoodsModel, CartModel

from django.contrib.auth.models import User

from users.serializers import OrderGoodsModelSerializer


def djlogin(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=name,
                                 password=password) #如果验证通过,返回user, 验证不通过返回none
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/users/home/')
        else:
            return HttpResponse('用户名或密码错误')


def djregist(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        if User.objects.filter(username=name).exists():
            return HttpResponse('用户名已经存在')
        else:
            password = request.POST.get('password')
            email = request.POST.get('email')
            icon = request.FILES.get('icon')
            User.objects.create_user(
                username=name,
                password=password,
                is_superuser=0,
                first_name = name,
                last_name = name,
                email= email,
                is_staff=1,
                is_active=1,
            )
            return render(request, 'home/home.html')


def djlogout(request):
    if request.method == 'GET':
        auth.logout(request)
        return render(request, 'home/home.html')


def foodtypes(request, i):
    if request.method == 'GET':
        path = request.path.split('/')[2]
        foodtypes = FoodType.objects.all()
        goods = Goods.objects.all()
        list_name = '综合排序'
        if i == '1' :
            goods = goods.order_by('-price')
            list_name = '价格降序'
        elif i == '2':
            goods = goods.order_by('price')
            list_name = '价格升序'
        elif i == '3':
            goods = goods.order_by('productnum')
            list_name = '销量排序'
        elif i == '4':
            goods = goods.order_by('storenums')
            list_name = '综合排序'
        return render(request, 'market/market.html', {'foodtypes': foodtypes, 'goods':goods, 'path':path, 'list_name':list_name})

def fenlei(request, typeid, i, k):
    if request.method == 'GET':
        path = request.path.split('/')[2] + '/' + request.path.split('/')[3]
        foodtypes = FoodType.objects.all()
        x = foodtypes.get(typeid=typeid).childtypenames.split('#')[1:]
        ms = {}
        for m in range(len(x)):
            fooname = (x[m].split(':')[0])
            fooid = (x[m].split(':')[1])
            ms[fooid] = fooname
        goods = Goods.objects.filter(categoryid=typeid)
        list_name = '综合排序'
        if i == '1' :
            goods = goods.order_by('-price')
            list_name = '价格降序'
        elif i == '2':
            goods = goods.order_by('price')
            list_name = '价格升序'
        elif i == '3':
            goods = goods.order_by('productnum')
            list_name = '销量排序'
        elif i == '4':
            goods = goods.order_by('storenums')
            list_name = '综合排序'
        if k != '0':
            goods = goods.filter(childcid=k)
            list1_name = ms[k]
        else:
            list1_name = '全部分类'
        return render(request, 'market/market.html', {'foodtypes': foodtypes, 'goods':goods, 'path': path, 'ms':ms, 'typeid':typeid, 'k':k, 'list_name':list_name, 'list1_name': list1_name})


def home(request):

    banners = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    mainshows = MainShow.objects.all()
    mainshops = MainShop.objects.all()
    return render(request, 'home/home.html',
                  {'banners': banners,
                   'navs':navs,
                   'mustbuys':mustbuys,
                   'mainshows':mainshows,
                   'mainshops':mainshops})


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        if UserModel.objects.filter(username=username).exists():
            return HttpResponse('用户名已经存在')
        else:
            password= request.POST.get('password')
            email = request.POST.get('email')
            icon = request.FILES.get('icon')
            UserModel.objects.create(
                username=username,
                password=make_password(password),
                email=email,
                icon=icon
            )
            return HttpResponseRedirect('/users/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                s = 'qwertyuiopasdfghjklzxcvbnm'
                ticket = ''
                for i in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket += str(now_time)
                response = HttpResponseRedirect('/users/home/')
                response.set_cookie('ticket', ticket, max_age=60000)
                user.t_ticket = ticket
                user.save()
                return response
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('用户名错误')




def logout(request):
    response = HttpResponseRedirect('/users/home/')
    response.delete_cookie('ticket')
    return response

def deal_mine(request):
    user = request.user
    nopay,waited = 0, 0
    if user.id:
        orders = user.ordermodel_set.all()
        if orders.first():
            for order in orders:
                if order.o_status == 0:
                    nopay += 1
                elif order.o_status == 1:
                    waited += 1
        user.nopay = nopay
        user.waited = waited
        user.order = orders
        return user

def mine(request):
    user = deal_mine(request)
    return render(request,  'mine/mine.html', {'user':user})


def cart(request):
    if request.method == 'GET':
        carts = CartModel.objects.all()
        totalprice = caltotal()
        data = {'carts':carts, 'totalprice':totalprice}
        return render(request, 'cart/cart.html', data)


def addnum(request):
    if request.method == 'POST':
        data = {
            'msg':'请求成功',
            'code':'200'
        }
        user = request.user
        if user.id:
            good_id = request.POST.get('good_id')
            carts = CartModel.objects.filter(user_id=user.id,goods_id=good_id)
            instance = carts.first()
            if carts.exists():
                instance.c_num += 1
                instance.save()
                data['c_num'] = instance.c_num
            else:
                CartModel.objects.create(
                    c_num=1,
                    is_select=1,
                    goods_id=good_id,
                    user_id=user.id
                )
                data['c_num'] = 1
            totalprice = caltotal()
            data['totalprice'] = round(totalprice,2)
            return JsonResponse(data)


def subnum(request):
    if request.method == 'POST':
        data = {
            'msg':'请求成功',
            'code':'200'
        }
        user = request.user
        if user.id:
            good_id = request.POST.get('good_id')
            carts = CartModel.objects.filter(user_id=user.id,goods_id=good_id)
            instance = carts.first()
            if carts.exists():
                instance.c_num -= 1
                instance.save()
                data['c_num'] = instance.c_num
                if instance.c_num == 0:
                    instance.delete()
            totalprice = caltotal()
            data['totalprice'] = round(totalprice,2)
            return JsonResponse(data)


def caltotal():
    totalprice = 0
    carts = CartModel.objects.all()
    for cart in carts:
        if cart.is_select:
            totalprice += (cart.c_num * cart.goods.price)
    return totalprice


def change(request):
    if request.method == 'POST':
        data = {
            'msg':'请求成功',
            'code':'200'
        }
        user = request.user
        if user.id:
            goods_id = request.POST.get('good_id')
            user_cart = CartModel.objects.get(user_id=user.id, goods_id=goods_id)
            user_cart.is_select = not user_cart.is_select
            user_cart.save()
            data['is_select'] = user_cart.is_select
            if user_cart.is_select:
                price = user_cart.goods.price
                midprice = user_cart.c_num * price
                data['midprice'] = midprice
            totalprice = caltotal()
            data['totalprice'] = round(totalprice,2)
            return JsonResponse(data)


def selectall(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        user = request.user
        if user.id:
            carts = CartModel.objects.all()
            for cart in carts:
                if not cart.is_select:
                    cart.is_select = not cart.is_select
                    cart.save()
            totalprice = caltotal()
            data['totalprice'] = round(totalprice,2)
            return JsonResponse(data)


def take_order(request):
    if request.method == 'GET':
        user = deal_mine(request)
        carts = CartModel.objects.filter(is_select=True)
        for cart in carts:
            if cart.is_select ==True:
                order = OrderModel.objects.create(
                    o_status=0,
                    o_create=time.time(),
                    user_id=user.id
                )
                for cart in carts:
                    OrderGoodsModel.objects.create(
                        goods_num=cart.c_num,
                        goods_id=cart.goods_id,
                        order_id=order.id
                    )
                totalprice = caltotal()
                carts.delete()
                ordergoods = OrderGoodsModel.objects.filter(order_id=order.id)
                data = {
                    'id':order.id,
                    'ordergoods': ordergoods,
                    'totalprice':round(totalprice,2),
                    'user' : deal_mine(request)
                }
                return render(request, 'order/order_info.html', data)
        return render(request, 'mine/mine.html', {'user':user})


def alipay(request, id):
    if request.method == 'GET':
        user = request.user
        if user.id:
            order = OrderModel.objects.filter(id=id).first()
            order.o_status = 1
            order.save()
            user = deal_mine(request)
            return render(request, 'mine/mine.html', {'user':user})


def wait_pay(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            ordergoods = OrderGoodsModel.objects.filter(order__o_status=0)
            orders = OrderModel.objects.filter(o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'orders':orders})


def wait_send(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            orders = OrderModel.objects.filter(o_status=1)
            return render(request, 'order/order_list_payed.html', {'orders':orders})