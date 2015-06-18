# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0006_authcounter'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpub',
            name='aaid',
            field=models.CharField(default=None, max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpub',
            name='regCounter',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\xbb\x91\xe5\xae\x9a\xe8\xae\xa1\xe6\x95\xb0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpub',
            name='signCounter',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\xad\xbe\xe5\x90\x8d\xe8\xae\xa1\xe6\x95\xb0'),
            preserve_default=True,
        ),
    ]
