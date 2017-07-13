# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify


class Brand(models.Model):
	name = models.CharField(max_length=250)
	title = models.CharField(max_length=250 , blank=True)
	description  = models.TextField(blank=True, null=True)
	slug = models.SlugField(max_length=128, unique=True)
	
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Brand, self).save(*args, **kwargs)  

	def __str__(self):
		return self.name


class Item(models.Model):
	brand = models.ForeignKey(Brand, related_name='+')
	name = models.CharField(max_length=250)
	title = models.CharField(max_length=250 , blank=True, null=True)
	description  = models.TextField(blank=True, null=True)		
	slug = models.SlugField(max_length=128, unique=True)
	image  = models.ImageField(	upload_to = 'images/', null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Item, self).save(*args, **kwargs)  

	def __str__(self):
		return self.name

