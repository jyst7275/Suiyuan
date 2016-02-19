from django.http import HttpResponse
from django.template import RequestContext, loader
from .model import Passage, Topnews, Flownews, Product, ProductCategory, Hotproduct, RecommendProduct
from django.template.defaulttags import register
from django.db.models import Q
import qrcode as qrcode_maker
from io import BytesIO
import datetime
import math


@register.filter
def oper_minus(a, b):
	return a - b


@register.filter
def oper_plus(a, b):
	return a + b


@register.filter
def get_point(item, key):
	return item.key


@register.filter
def get_item_index(a):
	return a.index


@register.filter
def item_eq(a, b):
	return a == b


@register.filter
def get_item(dic, key):
	return dic.get(key)


@register.filter
def get_range(value):
	return range(value)


@register.filter
def get_be(left, right):
	return left >= right


def index(request):
	template = loader.get_template('suiyuan/index.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))


def news(request):
	template = loader.get_template('suiyuan/news.html')
	pass_all = Passage.objects.filter(pass_status="published")
	type_list = ['app-active ', '', '', '']
	if request.method == 'GET':

		pass_type = request.GET.get('passage', '')
		if not pass_type == "":
			type_list[0] = ''
			pass_all = pass_all.filter(pass_type=pass_type)
		if pass_type == 'news':
			type_list[1] = 'app-active '
		elif pass_type == 'business':
			type_list[2] = 'app-active '
		elif pass_type == 'health':
			type_list[3] = 'app-active '

	top_news = Topnews.objects.latest('set_date')
	page_count = math.ceil(pass_all.count()/6)
	try:
		flow_news = Flownews.objects.all()
	except Flownews.DoesNotExist:
		flow_news = False
	return HttpResponse(template.render(RequestContext(request, {
		"passage_list": pass_all,
		"top_news": top_news,
		"flow_news": flow_news,
		"page_count": page_count,
		"type_list": type_list
	})))


def about(request):
	template = loader.get_template('suiyuan/about.html')
	return HttpResponse(template.render(RequestContext(request, {})))


def archives(request, year, month, day, title):
	template = loader.get_template('suiyuan/article.html')
	url = request.path
	object_get = Passage.objects.get(pass_title=title, pub_date__gte=datetime.datetime(int(year), int(month), int(day)))
	try:
		object_next = object_get.get_next_by_pub_date()
	except Passage.DoesNotExist:
		object_next = False
	try:
		object_prev = object_get.get_previous_by_pub_date()
	except Passage.DoesNotExist:
		object_prev = False
	return HttpResponse(template.render(RequestContext(request, {
		"passage": object_get,
		"passage_next": object_next,
		"passage_prev": object_prev,
		"current_url": url
	})))


def qrcode(request, url):
	get_num = '?action=qrcode'
	for key in request.GET:
		get_num += '&{0}={1}'.format(key, request.GET[key])
	url = "http://10.0.0.102:8080" + url + get_num
	img = qrcode_maker.make(url)
	buf = BytesIO()
	img.save(buf)
	image_stream = buf.getvalue()
	response = HttpResponse(image_stream, content_type='image/png')
	response['Last-Modified'] = 'Thu, 18 Feb 2016 02:05:03 GMT'
	response['Cache-Control'] = 'max-age=31536000'
	return response


def get_cat(fo):
	ca = fo.product_category
	if not ca.is_subclass:
		return ca
	else:
		return deep_cat(ca.father)


def deep_cat(fo):
	if not fo.is_subclass:
		return fo
	else:
		return deep_cat(fo.father)


def products(request):
	template = loader.get_template('suiyuan/products.html')
	product_dict = {}
	pc_dict = {}
	pc_list = ProductCategory.objects.all()
	product_list = Product.objects.filter(product_status="on")
	hot_list = Hotproduct.objects.all()
	for foo in product_list:
		main_ca = get_cat(foo)
		if main_ca in product_dict:
			product_dict[main_ca].append(foo)
		else:
			product_dict[main_ca] = [foo]
	for pc in pc_list:
		if not pc.is_subclass:
			if pc not in pc_dict:
				pc_dict[pc] = []
		else:
			fa = deep_cat(pc)
			if fa not in pc_dict:
				pc_dict[fa] = [pc]
			else:
				pc_dict[fa].append(pc)

	return HttpResponse(template.render(RequestContext(request, {
		"pc_list": pc_dict,
		"product_list": product_dict,
		"hot_list": hot_list
	})))


def contact(request):
	template = loader.get_template('suiyuan/contact.html')
	return HttpResponse(template.render(RequestContext(request, {})))


def people(request):
	template = loader.get_template('suiyuan/people.html')
	return HttpResponse(template.render(RequestContext(request, {})))


def product_archives(request, cat):
	order_ba = False
	order_di = ""
	if request.method == "GET" and "order-by" in request.GET:
		order_str = request.GET['order-by']
		order_arr = order_str.split('-')
		order = order_arr[0]
		order_direction = order_arr[1]
		if order == "price":
			order_ba = "product_prize"
		elif order == "date":
			order_ba = "product_date"
		if order_direction == "down":
			order_di = "-"
	template = loader.get_template('suiyuan/product_archive.html')
	pc_dict = {}
	pc_list = ProductCategory.objects.all()
	index_type_sub = "all"
	for pc in pc_list:
		if not pc.is_subclass:
			if pc not in pc_dict:
				pc_dict[pc] = []
		else:
			fa = deep_cat(pc)
			if fa not in pc_dict:
				pc_dict[fa] = [pc]
			else:
				pc_dict[fa].append(pc)
	if cat == "all":
		product_list = Product.objects.all()
		index_type = "all"
	else:
		pc_name = ProductCategory.objects.get(category=cat)
		if pc_name.is_subclass:
			index_type = pc_name.father.category
			index_type_sub = pc_name.category
		else:
			index_type = pc_name.category
		product_list = Product.objects.filter(Q(product_category__father__category=cat) | Q(product_category__category=cat))
	if order_ba != False:
		product_list = product_list.order_by(order_di + order_ba)
	return HttpResponse(template.render(RequestContext(request, {
		"product_list": product_list,
		"pc_list": pc_dict,
		"index_type": index_type,
		"index_type_sub": index_type_sub,
		"request_type": cat,
		"order": {"obj": order_ba, "direction": order_di}
	})))


def product_details(request, product_category, product_index):
	template = loader.get_template("suiyuan/product_detail.html")
	obj = Product.objects.get(product_index=product_index)

	recommend_list = RecommendProduct.objects.all()
	return HttpResponse(template.render(RequestContext(request, {
		"product": obj,
		"recommend_list": recommend_list,
		'current_url': '/order/confirm/?product='+product_index
	})))