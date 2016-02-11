from django.db import models
from django.utils import timezone
from uuslug import slugify
from django.utils.html import format_html


class PassageContent(models.Model):
	con_content = models.TextField()

	def __str__(self):
		if len(self.con_content) < 30:
			length = len(self.con_content)
		return self.con_content[0:30]


class Passage(models.Model):
	pub_date = models.DateTimeField('date published', default=timezone.now())
	pass_type = models.CharField(max_length=20, choices=(("News", "公司新闻"), ("Business", "行业动态"), ("Health", "健康知识")))
	pass_title = models.CharField(max_length=100)
	pass_summery = models.CharField(max_length=500)
	pass_img = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
	pass_content = models.OneToOneField(PassageContent, on_delete=models.CASCADE)
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
	product_img = models.ImageField(upload_to='uploads/product/')
	product_summery = models.CharField(max_length=200)
	product_description = models.TextField()
	product_prize = models.IntegerField()
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

	def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
		self.product_category.count += 1
		self.product_category.save()
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

