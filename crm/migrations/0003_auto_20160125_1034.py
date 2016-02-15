# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_default_gender'),
        ('crm', '0002_auto_20150607_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrmContact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact', models.OneToOneField(to='contact.Contact')),
                ('industry', models.ForeignKey(blank=True, to='crm.Industry', null=True)),
            ],
            options={
                'verbose_name_plural': 'CRM Contacts',
                'verbose_name': 'CRM Contact',
            },
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='user',
            field=models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
