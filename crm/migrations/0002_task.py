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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('recurrence', models.IntegerField(null=True, blank=True, choices=[(1, 'End of Month')])),
                ('due', models.DateField(null=True, blank=True)),
                ('complete', models.DateTimeField(null=True, blank=True)),
                ('complete_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('ticket', models.ForeignKey(to='crm.Ticket')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('user_assigned', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
    ]
