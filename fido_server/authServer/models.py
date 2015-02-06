#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models


class UserPub(models.Model):
    upid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name="用户名")
    aaid = models.CharField(max_length=50,default=None, verbose_name="设备号")
    publicKey = models.TextField(verbose_name="用户公钥")
    keyid = models.CharField(max_length=100, verbose_name="keyID")
    regCounter = models.IntegerField(default = 0,verbose_name="绑定计数")
    signCounter = models.IntegerField(default = 0,verbose_name="签名计数")
    isValidate = models.NullBooleanField(verbose_name="是否有效")
    extension = models.CharField(max_length=100)


class Policy(models.Model):
    pid = models.AutoField(primary_key=True)
    aaid = models.CharField(max_length=50, verbose_name="设备号")
    appid = models.URLField(verbose_name="应用编号")
    authFactor = models.PositiveIntegerField(verbose_name="认证因子")
    keyPro = models.PositiveIntegerField(verbose_name="密钥保护")
    attachment = models.PositiveIntegerField(verbose_name="附加类型")
    securDis = models.PositiveIntegerField(verbose_name="安全显示")
    allowed = models.NullBooleanField(verbose_name="是否允许")


class AuthAlgorithm(models.Model):
    alid = models.AutoField(primary_key=True)
    authalgs = models.PositiveIntegerField(verbose_name="认证算法")


class Scheme(models.Model):
    ssid = models.AutoField(primary_key=True)
    supportedScheme = models.PositiveIntegerField(verbose_name="认证方案")


class PolicyAlgs(models.Model):
    paid = models.AutoField(primary_key=True)
    pid = models.IntegerField(max_length=11, verbose_name="策略编号")
    alid = models.IntegerField(max_length=11, verbose_name="算法编号")


class PolicyScheme(models.Model):
    psid = models.AutoField(primary_key=True)
    pid = models.IntegerField(max_length=11, verbose_name="策略编号")
    ssid = models.IntegerField(max_length=11, verbose_name="方案编号")


class AuthMeta(models.Model):
    amid = models.AutoField(primary_key=True)
    aaid = models.CharField(max_length=50, verbose_name="设备号")
    certificate = models.TextField(verbose_name="设备证书")
    description = models.CharField(max_length=200, verbose_name="设备描述")
    veriMethod = models.PositiveIntegerField(verbose_name="认证方法")
    attachment = models.PositiveIntegerField(verbose_name="附加类型")
    keyPro = models.PositiveIntegerField(verbose_name="密钥保护")
    securDis = models.PositiveIntegerField(verbose_name="安全显示")
    disContentType = models.CharField(max_length=200, verbose_name="显示内容类型")
    ifSecond = models.NullBooleanField(verbose_name="第二认证")
    logo = models.CharField(max_length=40, verbose_name="标志")
    scheme = models.CharField(max_length=50, verbose_name="认证方案")
    authAlgs = models.PositiveIntegerField(verbose_name="认证算法")
    miniVer = models.CharField(max_length=5, verbose_name="最小版本")
    maxVer = models.CharField(max_length=5, verbose_name="最大版本")


class TrustedApps(models.Model):
    taid = models.AutoField(primary_key=True)
    appid = models.URLField(verbose_name="应用编号")
    facetid = models.CharField(max_length=100, verbose_name="facetId")


class authCounter(models.Model):
    acid = models.AutoField(primary_key=True)
    aaid = models.CharField(max_length=50, verbose_name="设备号")
    regCounter = models.IntegerField(verbose_name="绑定计数")
    signCounter = models.IntegerField(verbose_name="签名计数")
