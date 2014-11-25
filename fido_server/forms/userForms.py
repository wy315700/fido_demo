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
        
        

