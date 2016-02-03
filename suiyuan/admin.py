from django_summernote.admin import SummernoteModelAdmin
from .model import Passage
from .model import PassageContent
from .model import Topnews, Flownews, ProductCategory, Product, Hotproduct
from django.contrib import admin


admin.site.register(Topnews)
admin.site.register(Flownews)
admin.site.register(Hotproduct)
admin.site.register(ProductCategory)


class ProductAdmin(SummernoteModelAdmin):
	list_display = ("img_display", "product_name", "product_category", "product_prize",)
	list_display_links = ("img_display", "product_name")


class PassageAdmin(admin.ModelAdmin):
	fields = ('pub_date', ('pass_title', 'pass_type'), 'pass_summery', 'pass_img', 'pass_content')
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


admin.site.register(Product, ProductAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(PassageContent, PassageContentAdmin)
