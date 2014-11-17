#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

class FacetIDList (models.Model):
    id = models.AutoField(primary_key=True)
    facetId = models.CharField(max_length=100, verbose_name="facetId")
    class Meta:
        verbose_name_plural = 'facetId管理'
        verbose_name = 'facetId'
