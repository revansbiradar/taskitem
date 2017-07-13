"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from task import settings
from django.conf.urls.static import static
import api
from project import views	

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^accounts/login/$', views.login, name='account_login'),

	url(r'^brand/$', views.brandList, name='brand_list'),
	url(r'^add/brand/$', views.brandAdd, name='brand_add'),
	url(r'^edit/brand/(?P<id>\d+)/$', views.brandEdit, name='brand_edit'),
	# url(r'^delete/brand/(?P<id>\d+)/$', views.brandDelete, name='brand_delete'),

	url(r'^item/$', views.itemList, name='item_list'),
	url(r'^add/item/$', views.itemAdd, name='item_add'),
	url(r'^edit/item/(?P<id>\d+)/$', views.itemEdit, name='item_edit'),

	url(r'^admin/', admin.site.urls),

	# api's for user 
	url(r'^api/users/', api.UserList.as_view(), name="account_create"),
	url(r'^api/users/(?P<pk>[0-9]+)/$', api.UserDetail.as_view()),

	# api's for brand model
	url(r'^api/brands/', api.BrandList.as_view(), name="brandList"),
	url(r'^api/brands/(?P<pk>[0-9]+)/$', api.BrandDetail.as_view(), name="brandDetail"),

	# api's for item models
	url(r'^api/items/$', api.ItemList.as_view(), name="itemList"),
	url(r'^api/items/(?P<pk>[0-9]+)$', api.ItemDetail.as_view(), name="itemDetail"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
