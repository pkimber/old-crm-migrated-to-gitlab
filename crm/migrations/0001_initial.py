# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('mail', models.EmailField(blank=True, max_length=75)),
                ('hourly_rate', models.DecimalField(blank=True, max_digits=8, null=True, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'Contacts',
                'ordering': ('slug',),
                'verbose_name': 'Contact',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Industries',
                'ordering': ('name',),
                'verbose_name': 'Industry',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Notes',
                'ordering': ('created',),
                'verbose_name': 'Note',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('level', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Priorities',
                'ordering': ('-level', 'name'),
                'verbose_name': 'Priority',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('due', models.DateField(blank=True, null=True)),
                ('complete', models.DateTimeField(blank=True, null=True)),
                ('complete_user', models.ForeignKey(null=True, related_name='+', blank=True, to=settings.AUTH_USER_MODEL)),
                ('contact', models.ForeignKey(to='crm.Contact')),
                ('priority', models.ForeignKey(to='crm.Priority')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user_assigned', models.ForeignKey(null=True, related_name='+', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tickets',
                'ordering': ('-complete', 'due', '-priority__level', 'created'),
                'verbose_name': 'Ticket',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(to='crm.Contact')),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='note',
            name='ticket',
            field=models.ForeignKey(to='crm.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='industry',
            field=models.ForeignKey(null=True, blank=True, to='crm.Industry'),
            preserve_default=True,
        ),
    ]
