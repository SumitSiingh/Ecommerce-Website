from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder':'phone_no'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'email'}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'verify password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))

class ProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'pic']
        exclude = ['user']
