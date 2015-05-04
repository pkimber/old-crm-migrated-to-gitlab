# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('recurrence', models.IntegerField(blank=True, choices=[(1, 'End of Month')], null=True)),
                ('complete', models.DateTimeField(blank=True, null=True)),
                ('complete_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='+')),
                ('ticket', models.ForeignKey(to='crm.Ticket')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user_assigned', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='+')),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
            bases=(models.Model,),
        ),
    ]
