# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def _create_contact(model, obj):
    try:
        model.objects.get(slug=obj.slug)
    except model.DoesNotExist:
        print('\n{}\n'.format(obj.address.split('\n')))
        instance = model(**dict(
            name=obj.name,
            slug=obj.slug,
            url=obj.url,
            phone=obj.phone,
            mail=obj.mail,
            industry=obj.industry,
            hourly_rate=obj.hourly_rate,
        ))
        instance.save()
        instance.full_clean()


def transfer_to_new_contact_app(apps, schema_editor):
    contact_new = apps.get_model('contact', 'Contact')
    contact_old = apps.get_model('crm', 'Contact')
    for obj in contact_old.objects.all().order_by('pk'):
        _create_contact(contact_new, obj)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20151220_2043'),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
