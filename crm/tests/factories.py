# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.template.defaultfilters import slugify

import factory

from crm.models import Contact


class ContactFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Contact

    @factory.sequence
    def slug(n):
        return 'contact_{:02d}'.format(n)
