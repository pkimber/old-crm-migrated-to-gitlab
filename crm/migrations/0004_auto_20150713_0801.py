# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20150704_0036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='contact',
            new_name='crm_contact',
        ),
        migrations.RenameField(
            model_name='usercontact',
            old_name='contact',
            new_name='crm_contact',
        ),
    ]
