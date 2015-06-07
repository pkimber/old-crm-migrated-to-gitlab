# -*- encoding: utf-8 -*-
import factory

from decimal import Decimal

from crm.models import (
    Contact,
    Priority,
    Ticket,
)
from login.tests.factories import UserFactory


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
