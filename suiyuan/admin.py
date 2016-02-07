from django_summernote.admin import SummernoteModelAdmin
from .model import Passage
from .model import PassageContent
from .model import Topnews, Flownews, ProductCategory, Product, Hotproduct, RecommendProduct
from django.contrib import admin


class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ("category", "is_subclass", "img", "count", "father", "index")
	fields = ("category", "is_subclass", "img", "count", "father")


class ProductAdmin(SummernoteModelAdmin):
	list_display = ("img_display", "product_name", "product_category", "product_prize", "product_date")
	list_display_links = ("img_display", "product_name")


class PassageAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('pub_date', ('pass_title', 'pass_type'), 'pass_summery', 'pass_img', 'pass_content')
		}),
		('pic', {
			'classes': ('collapse',),
			'fields': ('img1', 'img2', 'img3', 'img4', 'img5')
		}),
		)

	list_display = ('pass_title', 'pub_date')
	view_on_site = True

	def formfield_for_choice_field(self, db_field, request=None, **kwargs):
		if db_field.name == "pass_type":
			kwargs['choices'] = (
				('News', '公司新闻'),
				('Business', '行业动态'),
				('Health', '健康知识'),
			)
		return super(PassageAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)


class PassageContentAdmin(SummernoteModelAdmin):
	pass

admin.site.register(Topnews)
admin.site.register(Flownews)
admin.site.register(Hotproduct)
admin.site.register(RecommendProduct)
admin.site.register(Product, ProductAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(PassageContent, PassageContentAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)