# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20150607_2042'),
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
        migrations.AlterField(
            model_name='usercontact',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user'),
        ),
    ]
