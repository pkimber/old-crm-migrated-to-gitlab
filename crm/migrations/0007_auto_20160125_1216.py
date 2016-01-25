# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20160125_1153'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='contact',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='new_contact',
            field=models.ForeignKey(related_name='ticket_contact', to=settings.CONTACT_MODEL),
        ),
    ]
