# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def _create_contact(model, obj, crm_model, user_model):
    user_name = obj.slug
    try:
        user = user_model.objects.get(username=user_name)
    except user_model.DoesNotExist:
        user = user_model(
            username=user_name,
            email=obj.mail,
            password=make_password(None),
            is_active=False,
            is_staff=False,
        )
        user.save()
        user.full_clean()
    # contact
    try:
        instance = model.objects.get(slug=obj.slug)
    except model.DoesNotExist:
        instance = model(**dict(
            user=user,
            company_name=obj.name,
            slug=obj.slug,
            website=obj.url or '',
            phone=obj.phone,
            # industry=obj.industry,
            hourly_rate=obj.hourly_rate,
        ))
        instance.save()
        instance.full_clean()
    # crm contact
    try:
        crm_model.objects.get(contact=instance)
    except crm_model.DoesNotExist:
        crm = crm_model(**dict(
            contact=instance,
            industry=obj.industry,
            hourly_rate=obj.hourly_rate,
        ))
        crm.save()
        crm.full_clean()


def transfer_to_new_contact_app(apps, schema_editor):
    contact_new = apps.get_model('contact', 'Contact')
    contact_old = apps.get_model('crm', 'Contact')
    crm_model = apps.get_model('crm', 'ContactCrm')
    user_model = apps.get_model(settings.AUTH_USER_MODEL)
    for obj in contact_old.objects.all().order_by('pk'):
        _create_contact(contact_new, obj, crm_model, user_model)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_contactcrm'),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
