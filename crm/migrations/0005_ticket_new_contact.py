# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_default_gender'),
        ('crm', '0004_auto_20160125_1040'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='new_contact',
            field=models.ForeignKey(blank=True, null=True, related_name='ticket_contact', to=settings.CONTACT_MODEL),
        ),
    ]
