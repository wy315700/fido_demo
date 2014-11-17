# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacetIDList',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('facetId', models.CharField(max_length=100, verbose_name=b'facetId')),
            ],
            options={
                'verbose_name': 'facetId',
                'verbose_name_plural': 'facetId\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
    ]
