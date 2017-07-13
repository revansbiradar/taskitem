# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth as django_auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import Brand,Item
from forms import BrandForm, ItemForm, LoginForm


@login_required
def index(request, template="index.html", context={}):
	items = Item.objects.all()
	brands = Brand.objects.all()
	context = {
		'items': items,
		'brands':brands
		}
	return render(request, template, context)

def login(request, template="accountLogin.html", context={}):
    next_url = request.GET.get('next', False)
    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = django_auth.authenticate(username=username, password=password)
            print user
            if user is not None:
                if user.is_active:
                    django_auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, _('You have successfully logged in.'))
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect(reverse('index'))
                else:
                    messages.add_message(request, messages.WARNING, _('Non active user.'))
            else:
                messages.add_message(request, messages.ERROR, _('Wrong username or password.'))

    context['form'] = login_form
    return render(request, template, context)




@login_required
def brandList(request):
	brands = Brand.objects.all()
	return render(request, 'brand_list_partial.html', 
					{'brands': brands}
				)


@login_required
def brandAdd(request):
	if request.method == 'POST':
		form = BrandForm(request.POST, None)
		if form.is_valid():
			brand = form.save(commit=False)
			brand.title = form.cleaned_data['title']
			brand.description = form.cleaned_data['description']
			brand.save()
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = BrandForm()
		return render(request, 'brand_add_partial.html', {'form':form})

@login_required
def brandEdit(request, id):
	brand = get_object_or_404(Brand, id=id)
	if request.method == "POST":
		form = BrandForm(request.POST, instance=brand)
		if form.is_valid():
			brand = form.save(commit=False)
			brand.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = BrandForm(instance=brand)
	return render(request, 'brand_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})


@login_required
def itemList(request):
	items = Item.objects.all()
	return render(request, 'item_list_partial.html', 
					{'items': items}
				)


@login_required
def itemAdd(request):
	if request.method == 'POST':
		form = ItemForm(request.POST, None)
		if form.is_valid():
			item = form.save(commit=False)
			item.title = form.cleaned_data['title']
			item.description = form.cleaned_data['description']
			item.save()
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = ItemForm()
		return render(request, 'item_add_partial.html', {'form':form})

@login_required
def itemEdit(request, id):
	item = get_object_or_404(Item, id=id)
	if request.method == "POST":
		form = ItemForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save(commit=False)
			item.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = ItemForm(instance=item)
	return render(request, 'brand_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})




