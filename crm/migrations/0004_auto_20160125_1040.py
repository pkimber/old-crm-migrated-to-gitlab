# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import DataError, migrations, models


def _create_contact(user, slug, name, website, phone, model):
    try:
        obj = model.objects.get(slug=slug)
    except model.DoesNotExist:
        obj = model(**dict(
            user=user,
            company_name=name,
            slug=slug,
            website=website,
            phone=phone,
        ))
        # import pdb; pdb.set_trace()
        obj.save()
        obj.full_clean()
    return obj


def _create_contact_crm(contact, industry, model):
    try:
        model.objects.get(contact=contact)
    except model.DoesNotExist:
        obj = model(**dict(
            contact=contact,
            industry=industry,
        ))
        obj.save()
        obj.full_clean()


def _create_user(user_name, email, model):
    try:
        obj = model.objects.get(username=user_name)
    except model.DoesNotExist:
        obj = model(
            username=user_name,
            email=email,
            password=make_password(None),
            is_active=False,
            is_staff=False,
        )
        obj.save()
        obj.full_clean()
    return obj


def _create(pk, model_contact_old, model_contact_new, model_contact_crm, model_user):
    obj = model_contact_old.objects.get(pk=pk)
    slug = obj.slug
    website = obj.url or ''
    user = _create_user(slug, obj.mail, model_user)
    contact = _create_contact(user, slug, obj.name, website, obj.phone, model_contact_new)
    # address
    try:
        address = obj.address.split('\n')
        if len(address) > 0:
            contact.address_1 = address[0].strip()
            # if '1st Floor' in address[0]:
            # import pdb; pdb.set_trace()
        if len(address) > 1:
            contact.address_2 = address[1].strip()
        if len(address) > 2:
            contact.address_3 = address[2].strip()
        if len(address) > 3:
            contact.town = address[3].strip()
        if len(address) > 4:
            contact.county = address[4].strip()
        if len(address) > 5:
            # if not 'Young' in address[5]:
            contact.postcode = address[5].strip()
        if len(address) > 6:
            # if not 'Young' in address[5]:
            contact.country = address[6].strip()
        contact.save()
        _create_contact_crm(contact, obj.industry, model_contact_crm)
    except DataError:
        print("Cannot save address '{}' (postcode is '{}')".format(
            address,
            address[5],
        ))
        raise


def transfer_to_new_contact_app(apps, schema_editor):
    model_contact_crm = apps.get_model('crm', 'CrmContact')
    model_contact_new = apps.get_model(settings.CONTACT_MODEL)
    model_contact_old = apps.get_model('crm', 'Contact')
    model_user = apps.get_model(settings.AUTH_USER_MODEL)
    pks = [obj.pk for obj in model_contact_old.objects.all().order_by('pk')]
    for pk in pks:
        _create(pk, model_contact_old, model_contact_new, model_contact_crm, model_user)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20160125_1034'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
