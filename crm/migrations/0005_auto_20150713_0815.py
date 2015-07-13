# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20150713_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='contact',
            field=models.ForeignKey(blank=True, to='crm.Contact', null=True),
        ),
        migrations.AddField(
            model_name='usercontact',
            name='contact',
            field=models.ForeignKey(blank=True, to='crm.Contact', null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='crm_contact',
            field=models.ForeignKey(related_name='crm_contact_ticket', to='crm.Contact'),
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='crm_contact',
            field=models.ForeignKey(related_name='crm_contact_user_contact', to='crm.Contact'),
        ),
    ]
