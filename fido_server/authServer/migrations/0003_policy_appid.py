# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0002_auto_20141120_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='appid',
            field=models.CharField(default='testAppID', max_length=50, verbose_name=b'\xe5\xba\x94\xe7\x94\xa8\xe7\xbc\x96\xe5\x8f\xb7'),
            preserve_default=False,
        ),
    ]
