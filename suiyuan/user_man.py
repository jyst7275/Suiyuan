from .model import SyUser, UserCode
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as userlogin
from django.contrib.auth import logout as userlogout
from django.contrib.auth import authenticate
from django import forms
from django.http import QueryDict
from django.shortcuts import render
from .model import Product, Address, Order,OrderDetail, RecommendProduct, OrderPay
from random import choice
from django.utils import timezone
from django.core.paginator import Paginator
import top, top.api
import random
import urllib.parse
import json
import requests
import hashlib


class LoginForm(forms.Form):
	cellphone = forms.CharField(label='手机号码（仅限中国大陆）')
	code = forms.CharField(label='验证码')


class UserBackend(object):
	def authenticate(self, cellphone=None, code_input=None):
		try:
			code = UserCode.objects.get(usercode=cellphone)
		except UserCode.DoesNotExist:
			return None
		if not code.code == code_input:
			return None
		try:
			user = SyUser.objects.get(cellphone=cellphone)
		except SyUser.DoesNotExist:
			user = SyUser(cellphone=cellphone, password="no password")
			user.save()
		return user

	def get_user(self, ky):
		try:
			return SyUser.objects.get(pk=ky)
		except SyUser.DoesNotExist:
			return None


def login(request):
	redirect_url = '/user/profile/'
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cell = request.POST['cellphone']
			code = request.POST['code']
			user = authenticate(cellphone=cell, code_input=code)
			if user is not None:
				userlogin(request, user)
				if 'redirect' in request.POST:
					redirect_url = request.POST['redirect']
				return HttpResponseRedirect(redirect_url)
	else:
		if 'redirect_to' in request.GET:
			redirect_url = request.GET['redirect_to']
		form = LoginForm()
	login_bool = request.user.is_authenticated()
	if login_bool:
		login_user = request.user.cellphone
	else:
		login_user = None
	return render(request, 'suiyuan/login.html', {
		'form': form,
		'redirect': redirect_url,
		'login_bool': login_bool,
		'user':login_user
	})


@login_required(redirect_field_name="redirect_to")
def status(request):
	return HttpResponse(request.user.is_authenticated())


def cart_to_view(cart_id_list, cart_count_list):
	return_cart = []
	total = 0
	total_count = 0
	if len(cart_id_list) != len(cart_count_list):
		raise KeyError

	for i, pr in enumerate(cart_id_list):
		product = Product.objects.get(product_index=pr)
		count = int(cart_count_list[i])
		if count <= 0:
			raise KeyError
		pr_total = product.product_prize * count
		total += pr_total
		total_count += count
		return_cart.append({
			'product': product,
			'count': count,
			'total': pr_total
		})
	return return_cart, total, total_count


def order_confirm(request):
	if not request.user.is_authenticated():
		if request.method == 'GET':
			get_dict = request.GET
			url_get = ""
			for i in get_dict:
				url_get += "&&" + i + "=" + get_dict[i]
			if not url_get == "":
				url_get = "?" + url_get[2:]
			url_get_encode = urllib.parse.quote(url_get)
			return HttpResponseRedirect('/user/login/?redirect_to=/order/confirm/' + url_get_encode)
		elif request.method == 'POST':
			cart_id = request.POST['id']
			cart_count = request.POST['count']
			cart_id_list = cart_id.split(',')
			cart_count_list = cart_count.split(',')
			request.session['order_confirm'] = {
				'cart_id_list': cart_id_list,
				'cart_count_list': cart_count_list
			}
			return HttpResponseRedirect('/user/login/?redirect_to=/order/confirm/' + urllib.parse.quote("?action=post"))
		return HttpResponseRedirect('/user/login/')

	if request.method == 'GET':
		if 'product' in request.GET:
			pr_id = get_object_or_404(Product, product_index=request.GET['product'])
			return_cart = [{
				'product': pr_id,
				'count': 1,
				'total': pr_id.product_prize
			}]
			total_count = 1
			total = pr_id.product_prize
		elif 'action' in request.GET:
			if request.GET['action'] == "post":
				try:
					return_cart, total, total_count = cart_to_view(request.session['order_confirm']['cart_id_list'], request.session['order_confirm']['cart_count_list'])
					del request.session['order_confirm']
				except KeyError:
					return SuspiciousOperation
			else:
				raise SuspiciousOperation
		else:
			raise SuspiciousOperation
	elif request.method == 'POST':
		if 'cart_pk' not in request.session:
			return HttpResponseRedirect('/user/cart/')
		if not request.POST.get('cart_pk') == request.session['cart_pk']:
			return HttpResponseRedirect('/user/cart/')
		del request.session['cart_pk']
		cart_id = request.POST['id']
		cart_count = request.POST['count']
		cart_id_list = cart_id.split(',')
		cart_count_list = cart_count.split(',')
		try:
			return_cart, total, total_count = cart_to_view(cart_id_list, cart_count_list)
		except KeyError or Product.DoesNotExist:
			raise SuspiciousOperation
	else:
		raise SuspiciousOperation
	address = Address.objects.filter(user=request.user)
	data_index = ''.join([choice('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxyZz0123456789') for i in range(20)])
	request.session['order_pk'] = data_index
	return render(request, "suiyuan/order_confirm.html", {
		'order': return_cart,
		'total': total,
		'total_count': total_count,
		'address': address,
		'order_pk': data_index
	})


@login_required(redirect_field_name='redirect_to')
def order_address(request):
	if request.method != 'POST':
		raise Http404
	else:
		try:
			name = request.POST['name']
			province = request.POST['province']
			city = request.POST['city']
			country = request.POST['country']
			detail = request.POST['detail']
			cellphone = request.POST['cellphone']
		except KeyError:
			raise SuspiciousOperation
		address = Address.objects.create(name=name, province=province, city=city, country=country, detail=detail, cellphone=cellphone, user=request.user)
		address.save()
	return_json = {
		'short': name + ' ' + province+city,
		'long': province+city+country+detail,
		'name': name,
		'cellphone': cellphone,
		'address_id': address.data_index
	}

	return HttpResponse(json.dumps(return_json))


@login_required(redirect_field_name='redirect_to')
def address_oper(request, address_no):
	address = get_object_or_404(Address, data_index=address_no, user=request.user)
	if request.method == "GET":
		address_json = {
			'name': address.name,
			'province': address.province,
			'city': address.city,
			'country': address.country,
			'detail': address.detail,
			'cellphone': address.cellphone
		}
		return HttpResponse(json.dumps(address_json))
	elif request.method == "DELETE":
		address.delete()
		return HttpResponse()
	elif request.method == "PUT":
		put = QueryDict(request.body)
		name = put.get('name')
		province = put.get('province')
		city = put.get('city')
		country = put.get('country')
		detail = put.get('detail')
		cellphone = put.get('cellphone')
		address.cellphone = cellphone
		address.province = province
		address.city = city
		address.name = name
		address.country = country
		address.detail = detail
		address.save()
	else:
		raise SuspiciousOperation
	return HttpResponse(json.dumps({
		'short': name + ' ' + province+city,
		'long': province+city+country+detail,
		'name': name,
		'cellphone': cellphone,
		'address_id': address.data_index
	}))


@login_required(redirect_field_name='redirect_to')
def order_request(request):
	if request.method != 'POST':
		raise SuspiciousOperation

	#check code
	if 'order_pk' not in request.session:
		raise SuspiciousOperation
	session_order_code = request.session['order_pk']
	del request.session['order_pk']
	if request.POST.get('order_pk') != session_order_code:
		raise SuspiciousOperation

	id_list = request.POST.get('id', '').split(',')
	count_list = request.POST.get('count', '').split(',')
	address = request.POST['address']
	try:
		address_obj = Address.objects.get(data_index=address)
	except Address.DoesNotExist:
		return SuspiciousOperation
	order = Order.objects.create(order_total=0, order_address=address_obj.short(), order_buyer=request.user,
	                             order_username= address_obj.name, order_pay=None, order_status="paying",
	                             order_cellphone=address_obj.cellphone)
	payment = request.POST.get('payment', '')
	if payment == "auto":
		add_pay("auto", order)
	order.save()
	total = 0
	try:
		for i, ids in enumerate(id_list):
			or_pr = Product.objects.get(product_index=ids)
			order_detail = OrderDetail.objects.create(order_id=order, order_product=or_pr, order_count=count_list[i], order_price=or_pr.product_prize)
			total += int(count_list[i]) * or_pr.product_prize
			order_detail.save()
	except Product.DoesNotExist:
		raise SuspiciousOperation
	order.order_total = total
	order.save()
	rp = RecommendProduct.objects.all()
	return_render = render(request, "suiyuan/order_finish.html", {
		'order': order,
		'rp': rp
	})
	if 'cart' in request.COOKIES:
		cookie = request.COOKIES['cart']
		mycart = json.loads(urllib.parse.unquote(cookie))
		for ids in id_list:
			if ids in mycart:
				del mycart[ids]
		return_render.set_cookie('cart', urllib.parse.quote(json.dumps(mycart)))
	return return_render


@login_required(redirect_field_name='redirect_to')
def order_detail(request, order_id):
	order = get_object_or_404(Order, order_buyer=request.user, order_index=order_id)
	order_detail = OrderDetail.objects.filter(order_id=order)
	if order.order_status == "paying":
		order_info = "您的订单已提交，请尽快付款"
	elif order.order_status == "waiting":
		order_info = "您的订单已确认，正等待系统处理"
	elif order.order_status == "processing":
		order_info = "系统已经处理了您的订单，等待出货中"
	elif order.order_status == "finished":
		order_info = "您的订单已出货，感谢您选择穗源"
	elif order.order_status == 'cancelpending':
		order_info = "您的取消请求已提交，正等待系统处理"
	elif order.order_status == 'canceled':
		order_info = "您的订单已取消"
	else:
		order_info = "订单状态异常，等待系统处理中"
	return render(request, "suiyuan/order_detail.html", {
		'order': order,
		'order_detail': order_detail,
		'order_info': order_info
	})


@login_required(redirect_field_name='redirect_to')
def profile(request):
	order_detail = {}
	order_detail_first = {}
	order_list_count = {}
	order_list = Order.objects.filter(order_buyer=request.user)
	selected = "all"
	page_now = 1
	if request.method == "GET":
		if "selected" in request.GET:
			selected = request.GET['selected']
			order_list = order_list.filter(order_status=selected)
		if "page" in request.GET:
			page_now = int(request.GET['page'])
	paginator = Paginator(order_list, 5)
	if not 0 <= page_now <= paginator.num_pages:
		raise Http404
	p = paginator.page(page_now)
	for order in p.object_list:
		detail = OrderDetail.objects.filter(order_id=order)
		order_list_count[order] = detail.count()
		order_detail[order] = []
		for i, obj in enumerate(detail):
			if i == 0:
				order_detail_first[order] = [obj]
			else:
				order_detail[order].append(obj)
	address = Address.objects.filter(user=request.user)

	selected_after = ''
	selected_list = ['', '', '', '', '']
	if selected == 'all':
		selected_list[0] = 'selected'
	elif selected == 'paying':
		selected_list[1] = 'selected'
	elif selected == 'waiting':
		selected_list[2] = 'selected'
	elif selected == 'processing':
		selected_list[3] = 'selected'
	elif selected == 'finished':
		selected_list[4] = 'selected'

	if not selected == "all":
		selected_after = "&selected=%s" % selected

	return render(request, "suiyuan/profile.html", {
		'order_list': p.object_list,
		'order_detail': order_detail,
		'order_detail_first': order_detail_first,
		'product_count': order_list_count,
		'address': address,
		'selected_after': selected_after,
		'selected_list': selected_list,
		'page_now': page_now,
		'page_total': paginator.num_pages,
		'has_next': p.has_next(),
		'has_prev': p.has_previous()
	})


def logout(request):
	userlogout(request)
	return HttpResponseRedirect('/user/login/')


def cart(request):
	try:
		cart_list_str = request.COOKIES['cart']
		cart_list_str = urllib.parse.unquote(cart_list_str)
		cart_list = json.loads(cart_list_str)
	except KeyError:
		cart_list = {}
	return_cart = []
	total = 0
	total_count = 0
	for cart_product in cart_list:
		count = cart_list[cart_product]
		try:
			product = Product.objects.get(product_index=cart_product)
			return_cart.append({'product': product, 'count': count, 'total': product.product_prize*count})
			total += product.product_prize*count
			total_count += count
		except Product.DoesNotExist:
			continue
	data_index = ''.join([choice('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxyZz0123456789') for i in range(20)])
	request.session['cart_pk'] = data_index
	return render(request, "suiyuan/cart.html", {
		'cart': return_cart,
		'total': total,
		'total_count': total_count,
		'cart_pk': data_index
	})


def sendcode_out(cellphone, code):
	mymd5 = hashlib.md5()
	mymd5.update(b'jy727580')
	password = mymd5.hexdigest()
	content = '您的验证码是：【%s】。请不要把验证码泄露给其他人。' % code
	sendvalue = {
		'method': 'Submit',
		'account': 'cf_jyst7275',
		'password': password,
		'mobile': cellphone,
		'content': content
	}
	url = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit'
	r = requests.post(url, sendvalue)
	print(r.content.decode('utf-8'))


def sendcode(cellphone, code):
	top.setDefaultAppInfo('23313828', '9c58da786b40f4d74bed1a7fb32ab7a1')
	top.getDefaultAppInfo()
	a = top.api.AlibabaAliqinFcSmsNumSendRequest()
	a.sms_type = "normal"
	a.sms_free_sign_name = "登录验证"
	a.sms_param = {
		"code": code,
		"product": "穗源购物"
	}
	a.rec_num = cellphone
	a.sms_template_code = "SMS_5048722"
	a.getResponse()


def user_code_gen(request, cellphone):
	try:
		code_before = UserCode.objects.get(usercode=cellphone)
		time_delta = (timezone.now() - code_before.last_request).seconds
		if time_delta <= 60:
			return HttpResponseBadRequest("请不要重复请求")
	except UserCode.DoesNotExist:
		pass
	if len(cellphone) == 11:
		code = random.randint(100000, 999999)
	else:
		return HttpResponse('None')
	try:
		usercode = UserCode.objects.get(usercode=cellphone)
		usercode.code = code
	except UserCode.DoesNotExist:
		usercode = UserCode.objects.create(usercode=cellphone, code=code)
	usercode.save()
	# sendcode(cellphone, str(code))
	return HttpResponse(json.dumps({'code': usercode.code, 'status': 'true'}))


def add_pay(method, order_obj, data=""):
	payment = OrderPay.objects.create(pay_method=method, pay_data=data)
	payment.save()
	order_obj.order_pay = payment
	order_obj.order_status = "waiting"


@login_required(redirect_field_name='redirect_to')
def address_location(request):
	if request.method != 'POST':
		raise SuspiciousOperation
	try:
		long = request.POST['long']
		lat = request.POST['lat']
		long = float(long) + 0.008774687519
		lat = float(lat) + 0.00374531687912
	except KeyError:
		raise SuspiciousOperation
	url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=u75trxs2Sm6TsanHVanYIopW&location={0},{1}'.format(lat,long)
	r = requests.get(url)
	r_json = r.json()
	address_json = {
		'province': r_json['result']['addressComponent']['province'],
		'city': r_json['result']['addressComponent']['city'],
		'country': r_json['result']['addressComponent']['district'],
		'detail': r_json['result']['formatted_address']
	}
	return HttpResponse(json.dumps(address_json))