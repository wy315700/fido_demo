#!/usr/bin/python  
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re

class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 20,
        widget = forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'username'}))
    password = forms.CharField(label = '密码', max_length = 25, 
        widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder' : 'password'}))

class RegistForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 20,
        widget = forms.TextInput(attrs = {'class':'form-control','placeholder':'username'}))
    email  = forms.EmailField(label = 'e-mail', required = False,
        widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email address'}))
    last_name = forms.CharField(label = '姓氏', max_length = 10, required = False,
        widget = forms.TextInput(attrs = {'class':'form-control','placeholder':'last_name'}))
    first_name = forms.CharField(label = '名字',max_length = 15, required = False,
        widget = forms.TextInput(attrs = {'class':'form-control','placeholder':'first_name'}))
    password = forms.CharField(label = '密码', max_length = 25,
        widget = forms.PasswordInput(attrs = {'class':'form-control','placeholder':'password'}))
    confirmPassword = forms.CharField(label = '确认密码', max_length = 25,
        widget = forms.PasswordInput(attrs = {'class':'form-control','placeholder':'confirm password'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("用户名只能由数字、字母和下划线组成！")
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        else:
            raise forms.ValidationError("用户名已存在！")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        else:
            raise forms.ValidationError("该邮箱已被注册！")

    def clean_confirmPassword(self):
        if self.cleaned_data['password']:
            confirmPassword = self.cleaned_data['confirmPassword']
            password = self.cleaned_data['password']
            print confirmPassword
            print password
            if confirmPassword == password:
                return confirmPassword
        raise forms.ValidationError("密码不匹配！")

        
        

