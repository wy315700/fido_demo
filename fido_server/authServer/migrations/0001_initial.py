# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAlgorithm',
            fields=[
                ('alid', models.AutoField(serialize=False, primary_key=True)),
                ('authalgs', models.PositiveIntegerField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe7\xae\x97\xe6\xb3\x95')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthMeta',
            fields=[
                ('amid', models.AutoField(serialize=False, primary_key=True)),
                ('aaid', models.IntegerField(max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('certificate', models.TextField(verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe8\xaf\x81\xe4\xb9\xa6')),
                ('description', models.CharField(max_length=200, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('veriMethod', models.PositiveIntegerField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe6\xb3\x95')),
                ('attachment', models.PositiveIntegerField(verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('keyPro', models.PositiveIntegerField(verbose_name=b'\xe5\xaf\x86\xe9\x92\xa5\xe4\xbf\x9d\xe6\x8a\xa4')),
                ('securDis', models.PositiveIntegerField(verbose_name=b'\xe5\xae\x89\xe5\x85\xa8\xe6\x98\xbe\xe7\xa4\xba')),
                ('disContentType', models.CharField(max_length=200, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe5\x86\x85\xe5\xae\xb9\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('ifSecond', models.NullBooleanField(verbose_name=b'\xe7\xac\xac\xe4\xba\x8c\xe8\xae\xa4\xe8\xaf\x81')),
                ('logo', models.CharField(max_length=40, verbose_name=b'\xe6\xa0\x87\xe5\xbf\x97')),
                ('scheme', models.CharField(max_length=50, verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe6\xa1\x88')),
                ('authAlgs', models.PositiveIntegerField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe7\xae\x97\xe6\xb3\x95')),
                ('miniVer', models.CharField(max_length=5, verbose_name=b'\xe6\x9c\x80\xe5\xb0\x8f\xe7\x89\x88\xe6\x9c\xac')),
                ('maxVer', models.CharField(max_length=5, verbose_name=b'\xe6\x9c\x80\xe5\xa4\xa7\xe7\x89\x88\xe6\x9c\xac')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('aaid', models.IntegerField(max_length=50, verbose_name=b'\xe8\xae\xbe\xe5\xa4\x87\xe5\x8f\xb7')),
                ('authFactor', models.PositiveIntegerField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe5\x9b\xa0\xe5\xad\x90')),
                ('keyPro', models.PositiveIntegerField(verbose_name=b'\xe5\xaf\x86\xe9\x92\xa5\xe4\xbf\x9d\xe6\x8a\xa4')),
                ('attachment', models.PositiveIntegerField(verbose_name=b'\xe9\x99\x84\xe5\x8a\xa0\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('securDis', models.PositiveIntegerField(verbose_name=b'\xe5\xae\x89\xe5\x85\xa8\xe6\x98\xbe\xe7\xa4\xba')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PolicyAlgs',
            fields=[
                ('paid', models.AutoField(serialize=False, primary_key=True)),
                ('pid', models.IntegerField(max_length=11, verbose_name=b'\xe7\xad\x96\xe7\x95\xa5\xe7\xbc\x96\xe5\x8f\xb7')),
                ('alid', models.IntegerField(max_length=11, verbose_name=b'\xe7\xae\x97\xe6\xb3\x95\xe7\xbc\x96\xe5\x8f\xb7')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PolicyScheme',
            fields=[
                ('psid', models.AutoField(serialize=False, primary_key=True)),
                ('pid', models.IntegerField(max_length=11, verbose_name=b'\xe7\xad\x96\xe7\x95\xa5\xe7\xbc\x96\xe5\x8f\xb7')),
                ('ssid', models.IntegerField(max_length=11, verbose_name=b'\xe6\x96\xb9\xe6\xa1\x88\xe7\xbc\x96\xe5\x8f\xb7')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('ssid', models.AutoField(serialize=False, primary_key=True)),
                ('supportedScheme', models.PositiveIntegerField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x96\xb9\xe6\xa1\x88')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPub',
            fields=[
                ('upid', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('publicKey', models.TextField(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x85\xac\xe9\x92\xa5')),
                ('keyid', models.CharField(max_length=100, verbose_name=b'keyID')),
                ('extension', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
