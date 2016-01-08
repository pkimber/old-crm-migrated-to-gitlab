# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def _create_contact(model, obj, user_model):
    try:
        model.objects.get(slug=obj.slug)
    except model.DoesNotExist:
        # user
        user = user_model(
            username=obj.mail or obj.slug,
            email=obj.mail,
            password=make_password(None),
            is_active=False,
            is_staff=False,
        )
        user.save()
        user.full_clean()
        # contact
        print('\n')
        print('{}           {}'.format(obj.slug, len(obj.slug)))
        print('  {}'.format(obj.address.split('\n')))
        print('  {}         {}'.format(obj.name, len(obj.name)))
        print('  {}         {}'.format(obj.url, len(obj.url)))
        print('  {}         {}'.format(obj.phone, len(obj.phone)))
        print('\n')
        instance = model(**dict(
            user=user,
            company_name=obj.name,
            slug=obj.slug,
            website=obj.url,
            phone=obj.phone,
            # industry=obj.industry,
            hourly_rate=obj.hourly_rate,
        ))
        instance.save()
        instance.full_clean()


def transfer_to_new_contact_app(apps, schema_editor):
    contact_new = apps.get_model('contact', 'Contact')
    contact_old = apps.get_model('crm', 'Contact')
    user_model = apps.get_model(settings.AUTH_USER_MODEL)
    for obj in contact_old.objects.all().order_by('pk'):
        _create_contact(contact_new, obj, user_model)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20151220_2043'),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
