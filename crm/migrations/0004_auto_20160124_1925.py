# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_default_gender'),
        ('crm', '0003_auto_20160124_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrmContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact', models.OneToOneField(to=settings.CONTACT_MODEL)),
                ('industry', models.ForeignKey(null=True, blank=True, to='crm.Industry')),
            ],
            options={
                'verbose_name_plural': 'CRM Contacts',
                'verbose_name': 'CRM Contact',
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='contact',
            field=models.ForeignKey(null=True, blank=True, to=settings.CONTACT_MODEL, related_name='ticket_contact'),
        ),
        migrations.AddField(
            model_name='usercontact',
            name='contact',
            field=models.ForeignKey(null=True, blank=True, to=settings.CONTACT_MODEL, related_name='user_contact_contact'),
        ),
    ]
