# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0005_auto_20141127_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='authCounter',
            fields=[
                ('acid', models.AutoField(serialize=False, primary_key=True)),
                ('aaid', models.CharField(max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('regCounter', models.IntegerField(verbose_name=b'\xe7\xbb\x91\xe5\xae\x9a\xe8\xae\xa1\xe6\x95\xb0')),
                ('signCounter', models.IntegerField(verbose_name=b'\xe7\xad\xbe\xe5\x90\x8d\xe8\xae\xa1\xe6\x95\xb0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
