from django.http import HttpResponse
from django.template import RequestContext, loader
from .model import Passage, Topnews, Flownews, Product, ProductCategory, Hotproduct
from django.template.defaulttags import register
from django.db.models import Q
import datetime
import math


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
	pass_all = Passage.objects.all()
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
		"page_count": page_count
	})))


def about(request):
	template = loader.get_template('suiyuan/about.html')
	return HttpResponse(template.render(RequestContext(request, {})))


def archives(request, year, month, day, index_pinyin):
	template = loader.get_template('suiyuan/article.html')
	object_get = Passage.objects.get(index_pinyin=index_pinyin, pub_date__gte=datetime.datetime(int(year), int(month), int(day)))
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
		"passage_prev": object_prev
	})))


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
	product_list = Product.objects.all()
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


def product_archives(request, index_pinyin):
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
	if index_pinyin == "all":
		product_list = Product.objects.all()
		index_type = "all"
	else:
		pc_name = ProductCategory.objects.get(index=index_pinyin)
		if pc_name.is_subclass:
			index_type = pc_name.father.index
			index_type_sub = pc_name.index
		else:
			index_type = pc_name.index
		product_list = Product.objects.filter(Q(product_category__father__index=index_pinyin) | Q(product_category__index=index_pinyin))
	if order_ba != False:
		product_list = product_list.order_by(order_di + order_ba)
	return HttpResponse(template.render(RequestContext(request, {
		"product_list": product_list,
		"pc_list": pc_dict,
		"index_type": index_type,
		"index_type_sub": index_type_sub,
		"request_type": index_pinyin,
		"order": {"obj": order_ba, "direction": order_di}
	})))