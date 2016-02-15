from .model import SyUser, UserCode
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from .model import UserCode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as userlogin
from django.contrib.auth import logout as userlogout
from django.contrib.auth import authenticate
from django import forms
from django.http import QueryDict
from django.shortcuts import render
from .model import Product, Address, Order,OrderDetail
import random
import urllib.parse
import json


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
	redirect_url = '/user/status/'
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cell = request.POST['cellphone']
			code = request.POST['code']
			user = authenticate(cellphone=cell, code_input=code)
			if user is not None:
				userlogin(request, user)
				if 'redirect_to' in request.POST:
					redirect_url = request.POST['redirect_url']
				return HttpResponseRedirect(redirect_url)
	else:
		if 'redirect_to' in request.GET:
			redirect_url = request.GET['redirect_to']
		form = LoginForm()
	return render(request, 'suiyuan/login.html', {'form': form, 'redirect': redirect_url})


@login_required(redirect_field_name="redirect_to")
def status(request):
	return HttpResponse(request.user.is_authenticated())


@login_required(redirect_field_name="redirect_to")
def order_confirm(request):
	if request.method != 'POST':
		return HttpResponseBadRequest()
	cart_id = request.POST['id']
	cart_count = request.POST['count']
	cart_id_list = cart_id.split(',')
	cart_count_list = cart_count.split(',')
	return_cart = []
	total = 0
	total_count = 0
	try:
		if len(cart_id_list) != len(cart_count_list):
			raise KeyError

		for i, pr in enumerate(cart_id_list):
			product = Product.objects.get(product_index=pr)
			count = int(cart_count_list[i])
			if count <= 0:
				raise KeyError
			pr_total = product.product_prize * count
			total += pr_total
			total_count + count
			return_cart.append({
				'product': product,
				'count': count,
				'total': pr_total
			})
	except KeyError or Product.DoesNotExist:
		return HttpResponseBadRequest()

	address = Address.objects.filter(user=request.user)
	return render(request, "suiyuan/order_confirm.html", {
		'order': return_cart,
		'total': total,
		'total_count': total_count,
		'address': address
	})


@login_required(redirect_field_name='redirect_to')
def order_address(request):
	if request.method != 'POST':
		return HttpResponseNotFound()
	else:
		try:
			name = request.POST['name']
			province = request.POST['province']
			city = request.POST['city']
			country = request.POST['country']
			detail = request.POST['detail']
			cellphone = request.POST['cellphone']
		except KeyError:
			return HttpResponseBadRequest()
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
	try:
		address = Address.objects.get(data_index=address_no, user=request.user)
	except Address.DoesNotExist:
		return HttpResponseBadRequest()
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
		return HttpResponseBadRequest()
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
		return HttpResponseBadRequest()

	id_list = request.POST.get('id', '').split(',')
	count_list = request.POST.get('count', '').split(',')
	address = request.POST['address']
	address_obj = Address.objects.get(id=int(address[-9:]))
	order = Order.objects.create(order_total=0, order_address=address_obj.short(), order_buyer=request.user, order_username=address_obj.name)
	order.save()
	total = 0
	for i, ids in enumerate(id_list):
		or_pr = Product.objects.get(product_index=ids)
		order_detail = OrderDetail.objects.create(order_id=order, order_product=or_pr, order_count=count_list[i], order_price=or_pr.product_prize)
		total += int(count_list[i]) * or_pr.product_prize
		order_detail.save()
	order.order_total = total
	order.save()
	return_render = render(request, "suiyuan/order_finish.html", {
		'order': order
	})
	if 'cart' in request.COOKIES:
		cookie = request.COOKIES['cart']
		mycart = json.loads(urllib.parse.unquote(cookie))
		for ids in id_list:
			if ids in mycart:
				del mycart[ids]
		return_render.set_cookie('cart', urllib.parse.quote(json.dumps(mycart)))
	return return_render


def logout(request):
	userlogout(request)
	return HttpResponse()


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

	return render(request, "suiyuan/cart.html", {'cart':return_cart, 'total':total, 'total_count':total_count})


def user_code_see(request, cellphone):
	usercode = UserCode.objects.get(usercode=cellphone)
	return HttpResponse(usercode.code)


def user_code_gen(request, cellphone):
	if len(cellphone) == 11:
		code = random.randint(100000,999999)
	else:
		return HttpResponse('None')
	try:
		usercode = UserCode.objects.get(usercode=cellphone)
		usercode.code = code
	except UserCode.DoesNotExist:
		usercode = UserCode.objects.create(usercode=cellphone,code=code)
	usercode.save()
	return HttpResponse(str(usercode.code))
