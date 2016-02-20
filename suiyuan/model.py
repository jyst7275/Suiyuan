from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from uuslug import slugify
from django.utils.html import format_html
from random import choice
from datetime import date


class ProductBanner(models.Model):
	banner_name = models.CharField('标签名', max_length=10)
	banner_img = models.ImageField('标签图', upload_to='uploads/banner/')

	class Meta:
		verbose_name_plural = '产品标签'
		verbose_name = '产品标签'

	def __str__(self):
		return self.banner_name


class UserCode(models.Model):
	usercode = models.CharField(max_length=20, primary_key=True)
	code = models.CharField(max_length=6)
	last_request = models.DateTimeField(auto_now=True)


class Passage(models.Model):
	pub_date = models.DateTimeField('日期', default=timezone.now())
	pass_type = models.CharField('文章类型', max_length=20, choices=(("News", "公司新闻"), ("Business", "行业动态"), ("Health", "健康知识")))
	pass_title = models.CharField('文章标题', max_length=100)
	pass_summery = models.CharField('文章简介', max_length=500)
	pass_img = models.ImageField('文章图片', upload_to='uploads/%Y/%m/%d/', null=True)
	pass_content = models.TextField('文章内容')
	pass_status = models.CharField('文章状态', max_length=20, choices=(
		("published", "发布"),
		('draft', "草稿"),
		('withdraw', "撤回")
	))

	class Meta:
		verbose_name = '文章管理'
		verbose_name_plural = '文章管理'

	def img_url(self):
		return self.pass_img.url

	def get_absolute_url(self):
		return "/archives/{0}/{1}/{2}/{3}".format(self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pass_title) + '/'

	def pass_url(self):
		return self.get_absolute_url()

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.index_pinyin = slugify(self.pass_title, max_length=60)
		super(Passage, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.pass_title


class Flownews(models.Model):
	passage = models.ForeignKey(Passage, on_delete=models.CASCADE, verbose_name='文章')

	class Meta:
		verbose_name = '滚动新闻'
		verbose_name_plural = '滚动新闻'

	def __str__(self):
		return self.passage.pass_title


class Topnews(models.Model):
	title = models.CharField('标题', max_length=100)
	summery = models.CharField('简介', max_length=500)
	set_date = models.DateTimeField('设置日期', default=timezone.now)
	passage = models.ForeignKey(Passage, on_delete=models.CASCADE, verbose_name='所选文章')

	class Meta:
		verbose_name = '最新消息'
		verbose_name_plural = '最新消息'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/news/'


class ProductCategory(models.Model):
	category = models.CharField('种类名', max_length=100)
	is_subclass = models.BooleanField('是否子类')
	img = models.ImageField('种类图片', upload_to='uploads/productCategory/')
	father = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name='父类别')

	class Meta:
		verbose_name = '产品种类'
		verbose_name_plural = '产品种类'

	def get_absolute_url(self):
		return "/products/archives/" + self.category + '/'

	def __str__(self):
		return self.category


class Product(models.Model):
	product_name = models.CharField('产品名', max_length=100)
	product_index = models.SlugField('产品id', max_length=100)
	product_img = models.ImageField('产品图片', upload_to='uploads/product/')
	product_summery = models.CharField('产品简介（很短）', max_length=200)
	product_description = models.TextField('产品介绍')
	product_prize = models.FloatField('产品价格')
	product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='产品种类')
	product_date = models.DateField("上市日期", default=timezone.datetime.today().date().replace(2012, 1, 1))
	product_status = models.CharField('产品状态', max_length=20, choices=(
		("on", "销售中"),
		('out', "已下架"),
		('off', "暂不可用")
	))
	img_1 = models.ImageField('产品图1', upload_to='uploads/product/', null=True, blank=True)
	img_2 = models.ImageField('产品图2', upload_to='uploads/product/', null=True, blank=True)
	img_3 = models.ImageField('产品图3', upload_to='uploads/product/', null=True, blank=True)
	img_4 = models.ImageField('产品图4', upload_to='uploads/product/', null=True, blank=True)
	img_5 = models.ImageField('产品图5', upload_to='uploads/product/', null=True, blank=True)

	class Meta:
		verbose_name = '产品'
		verbose_name_plural = '产品'

	def img_set(self):
		return [self.img_1, self.img_2, self.img_3, self.img_4, self.img_5]

	def get_absolute_url(self):
		return "/products/details/" + self.product_category.category + "/" + self.product_index + '/'

	def img_display(self):
		return format_html('<img src="{}" style="width:50px;">', self.product_img.url)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		pinyin = slugify(self.product_category.category,max_length=100)
		code = ""
		for word in pinyin.split('-'):
			first_letter = word[0].upper()
			code += first_letter
		data_index = code + ''.join([choice('0123456789') for i in range(5)])
		while not Product.objects.filter(product_index=data_index).count() == 0:
			data_index = code + ''.join([choice('0123456789') for i in range(5)])
		if not self.product_index:
			self.product_index = data_index
		super(Product, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.product_name


class RecommendProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品名')

	class Meta:
		verbose_name = '推荐产品'
		verbose_name_plural = '推荐产品'

	def __str__(self):
		return self.product.product_name


class Hotproduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品名')
	banner = models.ForeignKey(ProductBanner, on_delete=models.CASCADE, verbose_name='标签', null=True)

	class Meta:
		verbose_name_plural = '首页产品'
		verbose_name = '首页产品'

	def __str__(self):
		return self.product.product_name


class SyUserManager(BaseUserManager):
	def create_user(self, cellphone, password=None):
		if (not cellphone) or (not len(cellphone) == 11):
			raise ValueError('Cellphone Value Error!!')
		user = self.model(cellphone=cellphone)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, cellphone, username, password):
		user = self.create_user(cellphone, password)
		user.username = username
		user.is_admin = True
		user.save(using=self._db)
		return user


class SyUser(AbstractBaseUser):
	cellphone = models.CharField('手机号', max_length=20, unique=True)
	username = models.CharField('用户名', max_length=20,default='nobody')
	email = models.CharField('电子邮件', max_length=255)
	is_active = models.BooleanField('激活', default=True)
	is_admin = models.BooleanField('管理权限', default=False)

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = '用户'

	objects = SyUserManager()

	USERNAME_FIELD = 'cellphone'
	REQUIRED_FIELDS = ['username']

	def get_full_name(self):
		return self.username + ' ' + self.cellphone

	def get_short_name(self):
		return self.cellphone

	def __str__(self):
		return self.username + ' ' + self.cellphone

	def has_perm(self, perm, obj = None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin


class OrderPay(models.Model):
	pay_date = models.DateTimeField('付款日期')
	pay_method = models.CharField('付款方法', max_length=200)
	pay_data = models.CharField('付款数据', max_length=200)

	class Meta:
		verbose_name = '订单付款'
		verbose_name_plural = '订单付款'


class Order(models.Model):
	order_date = models.DateTimeField('订单日期', default=timezone.datetime.now())
	order_address = models.CharField('地址', max_length=100)
	order_total = models.FloatField('订单总额')
	order_buyer = models.ForeignKey(SyUser, on_delete=models.CASCADE, verbose_name='购买账户')
	order_username = models.CharField('收货人', max_length=10)
	order_index =models.SlugField('订单id', max_length=20, null=True)
	order_cellphone = models.CharField('联系人', max_length=20)
	order_status = models.CharField('订单状态', max_length=20, choices=(
		("paying", "待付款"),
		("waiting", "待处理"),
		("processing", "待出货"),
		("finished", "已完成"),
		("cancelpending", "取消请求中"),
		('canceled', '取消成功')
	))
	order_pay = models.OneToOneField(OrderPay, on_delete=models.CASCADE, null=True, verbose_name='付款详情')

	class Meta:
		verbose_name_plural = '订单'
		verbose_name = '订单'

	def status(self):
		search_dict = {
			"paying": "待付款",
			"waiting": "待处理",
			"processing": "待出货",
			"finished": "已完成",
			"cancelpending": "取消请求中",
			"canceled": "已取消"
		}
		return search_dict[self.order_status] if self.order_status in search_dict else None

	def order_detail(self):
		return_html = format_html('')
		detail_list = OrderDetail.objects.filter(order_id=self)
		for detail in detail_list:
			return_html += format_html('<li style="list-style:none;">{}{}{}</li>',
			detail.order_product.product_name, detail.order_count, detail.order_price)
		return format_html('<ul style="list-style: none;padding:0;margin:0;">') + return_html + format_html('</ul>')

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		data_index = date.today().strftime("%Y%m%d") + ''.join([choice('0123456789') for i in range(9)])
		while not Order.objects.filter(order_index=data_index).count() == 0:
			data_index = date.today().strftime("%Y%m%d") + ''.join([choice('0123456789') for i in range(9)])
		if not self.order_index:
			self.order_index = data_index
		super(Order, self).save(force_insert, force_update, using, update_fields)

	def get_absolute_url(self):
		return '/order/detail/' + self.order_index + '/'

	def __str__(self):
		return self.order_index


class OrderDetail(models.Model):
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='订单号')
	order_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
	order_count = models.IntegerField('数量')
	order_price = models.FloatField('单价')

	class Meta:
		verbose_name_plural = '订单详情'
		verbose_name = '订单详情'

	def __str__(self):
		return self.order_id.order_index + ' ' + self.order_product.product_name + ' ' + str(self.order_count)


class OrderStatus(models.Model):
	status_date = models.DateTimeField('时间', auto_now=True)
	status_name = models.CharField('行为', max_length=10)
	status_operator = models.CharField('操作人', max_length=20)


class Address(models.Model):
	name = models.CharField('收货人', max_length=20)
	province = models.CharField('省份', max_length=10)
	city = models.CharField('城市', max_length=10)
	country = models.CharField('县/区/市', max_length=10)
	detail = models.CharField('详细地址', max_length=50)
	cellphone = models.CharField('电话号码', max_length=20)
	user = models.ForeignKey(SyUser, on_delete=models.CASCADE, verbose_name='用户帐号')
	data_index = models.SlugField(max_length=20, null=True, verbose_name='地址id')

	class Meta:
		verbose_name_plural = '地址'
		verbose_name = '地址'

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not self.data_index:
			data_index = self.cellphone + ''.join([choice('0123456789') for i in range(9)])
			while not Address.objects.filter(data_index=data_index).count() == 0:
				data_index = self.cellphone + ''.join([choice('0123456789') for i in range(9)])
			self.data_index = data_index
		super(Address, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.name + ' ' + self.short()

	def short(self):
		return self.province+self.city+self.country+self.detail