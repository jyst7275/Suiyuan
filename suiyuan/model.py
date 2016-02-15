from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from uuslug import slugify
from django.utils.html import format_html


class UserCode(models.Model):
	usercode = models.CharField(max_length=20,primary_key=True)
	code = models.CharField(max_length=6)


class Passage(models.Model):
	pub_date = models.DateTimeField('date published', default=timezone.now())
	pass_type = models.CharField(max_length=20, choices=(("News", "公司新闻"), ("Business", "行业动态"), ("Health", "健康知识")))
	pass_title = models.CharField(max_length=100)
	pass_summery = models.CharField(max_length=500)
	pass_img = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
	pass_content = models.TextField()
	index_pinyin = models.SlugField(max_length=100, null=True)

	def img_url(self):
		return self.pass_img.url

	def get_absolute_url(self):
		return "/archives/{0}/{1}/{2}/{3}".format(self.pub_date.year, self.pub_date.month, self.pub_date.day, self.index_pinyin)

	def pass_url(self):
		return self.get_absolute_url()

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.index_pinyin = slugify(self.pass_title, max_length=60)
		super(Passage, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.pass_title


class Flownews(models.Model):
	passage = models.ForeignKey(Passage, on_delete=models.CASCADE)

	def __str__(self):
		return self.passage.pass_title


class Topnews(models.Model):
	title = models.CharField(max_length=100)
	summery = models.CharField(max_length=500)
	set_date = models.DateTimeField('Latest', default=timezone.now)
	passage = models.ForeignKey(Passage, on_delete=models.CASCADE)


class ProductCategory(models.Model):
	category = models.CharField(max_length=100)
	is_subclass = models.BooleanField()
	img = models.ImageField(upload_to='uploads/productCategory/')
	count = models.IntegerField()
	father = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
	index = models.SlugField(max_length=100, null=True)

	def get_absolute_url(self):
		return "/products/archives/" + self.category

	def __str__(self):
		return self.category

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.index = slugify(self.category, max_length=100)
		super(ProductCategory, self).save(force_insert, force_update, using, update_fields)


class Product(models.Model):
	product_name = models.CharField(max_length=100)
	product_index = models.SlugField(max_length=100, null=True)
	product_img = models.ImageField(upload_to='uploads/product/')
	product_summery = models.CharField(max_length=200)
	product_description = models.TextField()
	product_prize = models.FloatField()
	product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	product_date = models.DateField("Up_to_Market", default=timezone.datetime.today().date().replace(2012, 1, 1))
	img_1 = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
	img_2 = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
	img_3 = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
	img_4 = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
	img_5 = models.ImageField(upload_to='uploads/product/', null=True, blank=True)

	def img_set(self):
		return [self.img_1, self.img_2, self.img_3, self.img_4, self.img_5]

	def get_absolute_url(self):
		return "/products/details/" + self.product_category.category + "/" + str(self.id)

	def img_display(self):
		return format_html('<img src="{}" style="width:50px;">', self.product_img.url)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		pinyin = slugify(self.product_category.category,max_length=100)
		code = ""
		for word in pinyin.split('-'):
			first_letter = word[0].upper()
			code += first_letter
		super(Product, self).save(force_insert, force_update, using, update_fields)
		self.product_index = code + "%05d" % self.id
		super(Product, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.product_name


class RecommendProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.product.product_name


class Hotproduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

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
	cellphone = models.CharField(max_length=20, unique=True)
	username = models.CharField(max_length=20,default='nobody')
	email = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

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


class Order(models.Model):
	order_date = models.DateTimeField(default=timezone.datetime.now())
	order_address = models.CharField(max_length=100)
	order_total = models.FloatField()
	order_buyer = models.ForeignKey(SyUser, on_delete=models.CASCADE)
	order_username = models.CharField(max_length=10)
	order_index =models.SlugField(max_length=20, null=True)

	def order_detail(self):
		return_html = format_html('')
		detail_list = OrderDetail.objects.filter(order_id=self)
		for detail in detail_list:
			return_html += format_html('<li style="list-style:none;">{}{}{}</li>',
			detail.order_product.product_name, detail.order_count, detail.order_price)
		return format_html('<ul style="list-style: none;padding:0;margin:0;">') + return_html + format_html('</ul>')

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		super(Order, self).save(force_insert, force_update, using, update_fields)
		self.order_index = self.order_date.date().strftime('%Y%m%d') + "%09d" % self.id
		super(Order, self).save()

	def __str__(self):
		return self.order_index


class OrderDetail(models.Model):
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
	order_product = models.ForeignKey(Product, on_delete=models.CASCADE)
	order_count = models.IntegerField()
	order_price = models.FloatField()

	def __str__(self):
		return self.order_id.order_index + ' ' + self.order_product.product_name + ' ' + str(self.order_count)


class Address(models.Model):
	name = models.CharField(max_length=20)
	province = models.CharField(max_length=10)
	city = models.CharField(max_length=10)
	country = models.CharField(max_length=10)
	detail = models.CharField(max_length=50)
	cellphone = models.CharField(max_length=20)
	user = models.ForeignKey(SyUser, on_delete=models.CASCADE)
	data_index = models.SlugField(max_length=20, null=True)

	def __str__(self):
		return self.name + ' ' + self.short()

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		super(Address, self).save(force_insert, force_update, using, update_fields)
		self.data_index = self.cellphone + "%09d" % self.id
		super(Address, self).save()

	def short(self):
		return self.province+self.city+self.country+self.detail