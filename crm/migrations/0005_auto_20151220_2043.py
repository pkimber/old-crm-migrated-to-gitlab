# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('crm', '0004_auto_20150713_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, to='contact.Contact'),
        ),
        migrations.AddField(
            model_name='usercontact',
            name='contact',
            field=models.ForeignKey(related_name='contact', blank=True, null=True, to='contact.Contact'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='crm_contact',
            field=models.ForeignKey(related_name='crm_contact_ticket', blank=True, null=True, to='crm.Contact'),
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='crm_contact',
            field=models.ForeignKey(to='crm.Contact', related_name='crm_contact_user_contact'),
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='user',
            field=models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
