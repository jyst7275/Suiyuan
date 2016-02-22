"""suiyuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import rest
from . import user_man

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^news$', views.news),
    url(r'^archives/([0-9]+)/([0-9]+)/([0-9]+)/([\w|\-]+)/', views.archives),
    url(r'^about$', views.about),
    url(r'^products$', views.products),
    url(r'^products/archives/([\w|\-]+)/$', views.product_archives),
    url(r'^products/details/([\w|\-]+)/([\w|\-]+)/$', views.product_details),
    url(r'^user/login$', user_man.login),
    url(r'^user/logout$', user_man.logout),
    url(r'^user/status$', user_man.status),
    url(r'^user/cart$', user_man.cart),
    url(r'^user/profile$', user_man.profile),
    url(r'^order/detail/([0-9]+)$', user_man.order_detail),
    url(r'^order/confirm$', user_man.order_confirm),
    url(r'^order/request$',user_man.order_request),
    url(r'^v1/user/address$', user_man.order_address),
    url(r'^v1/user/address/location$', user_man.address_location),
    url(r'^v1/user/address/([0-9]+)$', user_man.address_oper),
    url(r'^v1/user/sendcode/([0-9]+)$', user_man.user_code_gen),
    url(r'^contact$', views.contact),
    url(r'^people$', views.people),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^v1/passage/([\w]+)$', rest.PassageDetail.as_view()),
    url(r'^v1/qrcode/(.+)$', views.qrcode),
    url(r'search$', views.search)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'suiyuan.views.my_500_view'
handler404 = 'suiyuan.views.my_404_view'
handler400 = 'suiyuan.views.my_400_view'
