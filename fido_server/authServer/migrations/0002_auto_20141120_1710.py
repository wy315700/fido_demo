# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authmeta',
            name='aaid',
            field=models.CharField(max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='policy',
            name='aaid',
            field=models.CharField(max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7'),
            preserve_default=True,
        ),
    ]
