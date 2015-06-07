# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20150607_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketTaskWarrior',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(unique=True)),
                ('ticket', models.OneToOneField(to='crm.Ticket')),
            ],
            options={
                'verbose_name_plural': 'Ticket TaskWarrior',
                'verbose_name': 'Ticket TaskWarrior',
                'ordering': ('ticket__pk',),
            },
        ),
    ]
