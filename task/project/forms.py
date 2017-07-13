from django import forms
from models import Brand, Item


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'