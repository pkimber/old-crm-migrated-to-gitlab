# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20160125_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='industry',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
