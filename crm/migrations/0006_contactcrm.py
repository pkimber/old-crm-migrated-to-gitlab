# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_default_gender'),
        ('crm', '0005_auto_20151220_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactCrm',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('contact', models.OneToOneField(to='contact.Contact')),
                ('industry', models.ForeignKey(null=True, blank=True, to='crm.Industry')),
            ],
            options={
                'verbose_name': 'CRM Contact',
                'verbose_name_plural': 'CRM Contacts',
            },
        ),
    ]
