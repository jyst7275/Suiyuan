from django_summernote.admin import SummernoteModelAdmin
from .model import Passage
from .model import Topnews, Flownews, ProductCategory, Product, Hotproduct, RecommendProduct
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .model import SyUser, Address, Order, OrderDetail, ProductBanner


class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ("category", "is_subclass", "img", "father")
	fields = ("category", "is_subclass", "img", "father")


class ProductAdmin(SummernoteModelAdmin):
	list_display = ("img_display", "product_name", "product_category", "product_prize", "product_date", "product_index", 'product_status')
	list_editable = ['product_status', 'product_prize']
	list_filter = ['product_category__category', 'product_status']
	list_display_links = ("img_display", "product_name")
	search_fields = ['product_category__category', 'product_name']
	fieldsets = (
		(None, {
			'fields': (('product_name', 'product_category', 'product_status'), 'product_prize', 'product_date', 'product_img',
			           'product_summery', 'product_description')
		}),
		('pic', {
			'classes': ('collapse',),
			'fields': ('img_1', 'img_2', 'img_3', 'img_4', 'img_5')
		}),
	)


class PassageAdmin(SummernoteModelAdmin):
	fields = ('pub_date', ('pass_title', 'pass_type', 'pass_status'), 'pass_summery', 'pass_img', 'pass_content', 'pass_title_index')

	list_display = ('pass_title', 'pub_date', 'pass_status')
	list_filter = ['pub_date', 'pass_status']
	list_editable = ['pass_status']
	view_on_site = True

	def formfield_for_choice_field(self, db_field, request=None, **kwargs):
		if db_field.name == "pass_type":
			kwargs['choices'] = (
				('News', '公司新闻'),
				('Business', '行业动态'),
				('Health', '健康知识'),
			)
		return super(PassageAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = SyUser
		fields = ('cellphone', 'username', 'email')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = SyUser
		fields = ('cellphone', 'username', 'email', 'password', 'is_active', 'is_admin')

	def clean_password(self):
		return self.initial["password"]


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('username', 'cellphone', 'is_admin')
	list_filter = ('is_admin', )
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal Info', {'fields': ('email', 'cellphone')}),
		('Permissions', {'fields': ('is_admin', )})
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('cellphone', 'username', 'email', 'password1', 'password2')
		}),
	)
	search_fields = ('cellphone',)
	ordering = ('cellphone', )
	filter_horizontal = ()


class OrderAdmin(admin.ModelAdmin):
	fields = ('order_index', ('order_buyer', 'order_username', 'order_cellphone'), 'order_date', 'order_address', 'order_total', 'order_status')
	list_display = ('order_index', 'order_date', 'order_detail', 'order_total', 'order_username', 'order_address', 'order_cellphone', 'order_status')
	search_fields = ['order_username', 'order_id', 'order_cellphone']
	list_editable = ['order_status']
	list_filter = ['order_status', 'order_date']
admin.site.register(SyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Topnews)
admin.site.register(Flownews)
admin.site.register(Hotproduct)
admin.site.register(ProductBanner)
admin.site.register(RecommendProduct)
admin.site.register(Product, ProductAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Address)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)