# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Brand, Item
# Register your models here.


class BrandAdmin(admin.ModelAdmin):
	list_display = (
		u'id', 
		'name',
		'title', 
		'description',
	)
admin.site.register(Brand, BrandAdmin)


class ItemAdmin(admin.ModelAdmin):
	list_display = (
		u'id', 
		'brand',
		'name',
		'title', 
		'description',
	)
admin.site.register(Item, ItemAdmin)
