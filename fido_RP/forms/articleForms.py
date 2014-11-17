#!/usr/bin/python  
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from articles.models import BaseCategory, Tag
import re

class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 20)
    password = forms.CharField(label = '密码', max_length = 25, widget = forms.PasswordInput())

class ArticleForm(forms.Form):
    categories = BaseCategory.objects.all()
    subject = forms.CharField(label = '文章标题', max_length = 50)
    isOrigin = forms.BooleanField(label = '是否原创', required = False)
    category = forms.ModelChoiceField(label = '分类', queryset = categories)
    status = forms.ChoiceField(choices = [('public', '公开'), ('limited', '受限'), ('private', '私密')])
    tag = forms.CharField(label = '标签', max_length = 50)
    content = forms.CharField(label = '内容', widget = forms.Textarea)

class CommentForm(forms.Form):
    content = forms.CharField(label = '评论内容', widget = forms.Textarea)
    essayId = forms.IntegerField(label = '文章ID')
    publisher = forms.IntegerField(label = '发布者')
    tend = forms.ChoiceField(choices = [('1', '赞'), ('0', '可以接受'), ('-1', '倒')])