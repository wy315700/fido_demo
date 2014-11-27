# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0004_auto_20141125_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrustedApps',
            fields=[
                ('taid', models.AutoField(serialize=False, primary_key=True)),
                ('appid', models.URLField(verbose_name=b'\xe5\xba\x94\xe7\x94\xa8\xe7\xbc\x96\xe5\x8f\xb7')),
                ('facetid', models.CharField(max_length=100, verbose_name=b'facetId')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='policy',
            name='appid',
            field=models.URLField(verbose_name=b'\xe5\xba\x94\xe7\x94\xa8\xe7\xbc\x96\xe5\x8f\xb7'),
            preserve_default=True,
        ),
    ]
