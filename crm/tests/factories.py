# -*- encoding: utf-8 -*-
from decimal import Decimal

from django.template.defaultfilters import slugify
from django.utils import timezone

import factory

from login.tests.factories import UserFactory

from crm.models import (
    Contact,
    Priority,
    Ticket,
)


class ContactFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Contact

    hourly_rate = Decimal('20.00')

    @factory.sequence
    def slug(n):
        return 'contact_{:02d}'.format(n)


class PriorityFactory(factory.django.DjangoModelFactory):

    level = 1

    class Meta:
        model = Priority

    @factory.sequence
    def name(n):
        return 'name_{:02d}'.format(n)


class TicketFactory(factory.django.DjangoModelFactory):

    contact = factory.SubFactory(ContactFactory)
    priority = factory.SubFactory(PriorityFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Ticket
