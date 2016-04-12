# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20160125_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercontact',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='usercontact',
            name='user',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='new_contact',
            new_name='contact',
        ),
        migrations.DeleteModel(
            name='UserContact',
        ),
    ]
