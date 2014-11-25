# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authServer', '0003_policy_appid'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='allowed',
            field=models.NullBooleanField(verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\x81\xe8\xae\xb8'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpub',
            name='isValidate',
            field=models.NullBooleanField(verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe6\x95\x88'),
            preserve_default=True,
        ),
    ]
