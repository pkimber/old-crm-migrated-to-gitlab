# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def _update(obj, model_contact_old, model_contact_new):
    contact_old = model_contact_old.objects.get(pk=obj.contact_id)
    contact_new = model_contact_new.objects.get(slug=contact_old.slug)
    obj.new_contact = contact_new
    obj.save()


def transfer_to_new_contact_app(apps, schema_editor):
    model_ticket = apps.get_model('crm', 'Ticket')
    model_contact_new = apps.get_model(settings.CONTACT_MODEL)
    model_contact_old = apps.get_model('crm', 'Contact')
    pks = [obj.pk for obj in model_ticket.objects.all().order_by('pk')]
    for pk in pks:
        ticket = model_ticket.objects.get(pk=pk)
        _update(ticket, model_contact_old, model_contact_new)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_ticket_new_contact'),
        ('invoice', '0007_invoice_new_contact'),
        migrations.swappable_dependency(settings.CONTACT_MODEL),
    ]

    operations = [
        migrations.RunPython(transfer_to_new_contact_app),
    ]
