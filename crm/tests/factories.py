# -*- encoding: utf-8 -*-
import factory

from decimal import Decimal
from django.conf import settings

from crm.models import Note, Priority, Ticket
from contact.tests.factories import ContactFactory
from login.tests.factories import UserFactory


# class CrmContactFactory(factory.django.DjangoModelFactory):
#
#     class Meta:
#         model = Contact
#
#     hourly_rate = Decimal('20.00')
#
#     @factory.sequence
#     def slug(n):
#         return 'contact_{:02d}'.format(n)


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


class NoteFactory(factory.django.DjangoModelFactory):

    ticket = factory.SubFactory(TicketFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Note

    @factory.sequence
    def title(n):
        return 'title_{:02d}'.format(n)
