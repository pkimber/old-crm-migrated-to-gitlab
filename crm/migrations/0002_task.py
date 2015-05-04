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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('recurrence', models.IntegerField(choices=[(1, 'End of Month')], blank=True, null=True)),
                ('due', models.DateTimeField(blank=True, null=True)),
                ('complete', models.DateTimeField(blank=True, null=True)),
                ('complete_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('ticket', models.ForeignKey(to='crm.Ticket')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user_assigned', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Task',
                'ordering': ('created',),
                'verbose_name_plural': 'Tasks',
            },
            bases=(models.Model,),
        ),
    ]
