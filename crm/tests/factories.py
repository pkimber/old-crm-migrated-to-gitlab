# -*- encoding: utf-8 -*-
import factory

from crm.models import CrmContact, Industry, Note, Priority, Ticket
from contact.tests.factories import ContactFactory
from login.tests.factories import UserFactory


class IndustryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Industry

    @factory.sequence
    def name(n):
        return 'name_{:02d}'.format(n)


class CrmContactFactory(factory.django.DjangoModelFactory):

    industry = factory.SubFactory(IndustryFactory)

    class Meta:
        model = CrmContact


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
