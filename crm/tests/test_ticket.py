# -*- encoding: utf-8 -*-
import pytest

from datetime import date
from django.test import TestCase
from django.utils import timezone

from contact.tests.factories import ContactFactory
from crm.models import Ticket
from crm.tests.factories import TicketFactory
from search.tests.helper import check_search_methods


@pytest.mark.django_db
def test_contact():
    contact = ContactFactory()
    TicketFactory(contact=contact, due=date.today(), title='t1')
    TicketFactory(contact=contact, title='t2')
    TicketFactory(complete=timezone.now(), title='t3')
    TicketFactory(title='t4')
    qs = Ticket.objects.contact(contact)
    assert ['t2', 't1'] == [obj.title for obj in qs]


@pytest.mark.django_db
def test_due():
    ticket = TicketFactory(due=date.today())
    assert not ticket.is_overdue


@pytest.mark.django_db
def test_overdue():
    ticket = TicketFactory(due=date(2010, 1, 1))
    assert ticket.is_overdue


@pytest.mark.django_db
def test_search_methods():
    check_search_methods(TicketFactory())


@pytest.mark.django_db
def test_str():
    str(TicketFactory())
