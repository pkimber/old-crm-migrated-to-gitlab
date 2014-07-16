# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.template.defaultfilters import slugify

import factory

from crm.models import Contact


class ContactFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Contact

    hourly_rate = Decimal('20.00')

    @factory.sequence
    def slug(n):
        return 'contact_{:02d}'.format(n)
