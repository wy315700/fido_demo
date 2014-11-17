#!/usr/bin/python  
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class BaseCategory(models.Model):
    id = models.AutoField(primary_key = True)
    base_name = models.CharField(max_length = 20, verbose_name = "类名")
    description = models.CharField(max_length = 100, verbose_name = "描述")
    class Meta:
        verbose_name_plural = '分类管理'
        verbose_name = '分类'
    def __unicode__(self):
        return self.base_name

class Tag(models.Model):
    id = models.AutoField(primary_key = True)
    tag_name = models.CharField(max_length = 20, verbose_name = "标签名")
    category = models.IntegerField(verbose_name = "所属分类")

class Essay(models.Model):
    id = models.AutoField(primary_key = True)
    subject = models.CharField(max_length = 50, verbose_name = "题目")
    type = models.BooleanField(verbose_name = "是否原创")
    category = models.ForeignKey(BaseCategory, verbose_name = "分类")
    content = models.TextField(verbose_name = "文章内容")
    modification_date = models.DateField(verbose_name = "修改时间")
    publish_date = models.DateField(verbose_name = "发布时间")
    essay_status = models.CharField(max_length = 10, verbose_name = "文章状态")
    class Meta:
        verbose_name_plural = '文章管理'
        verbose_name = '文章'
    def __unicode__(self):
        return self.subject

class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    essay = models.ForeignKey(Essay, verbose_name = "所属文章")
    publisher = models.ForeignKey(User, verbose_name = "评论人")
    support_num = models.IntegerField(verbose_name = "赞")
    tend = models.IntegerField(verbose_name = "态度")
    content = models.TextField(verbose_name = "评论内容")
    publish_time = models.DateTimeField(verbose_name = "发布时间")
    class Meta:
        verbose_name_plural = '评论管理'
        verbose_name = '评论'
    def __unicode__(self):
        title = self.content
        if len(title) > 10:
            title = title[0 : 10] + '...'
        return title

class tagEssayRelation(models.Model):
    essayId = models.ForeignKey(Essay, verbose_name = "文章ID")
    tagId = models.ForeignKey(Tag, verbose_name = "标签ID")

class supportCommentRelation(models.Model):
    commentId = models.ForeignKey(Comment, verbose_name = "评论Id")
    userId = models.ForeignKey(User, verbose_name = "用户Id")

class FacetIDs (models.Model):
    id = models.AutoField(primary_key=True)
    facetId = models.CharField(max_length=100, verbose_name="facetId")
    class Meta:
        verbose_name_plural = 'facetId管理'
        verbose_name = 'facetId'







