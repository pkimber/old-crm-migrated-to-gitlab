# -*- encoding: utf-8 -*-
import pytest

from datetime import date
from django.utils import timezone

from crm.tests.factories import (
    TaskFactory,
    TicketFactory,
)
from login.tests.factories import UserFactory
from search.tests.helper import check_search_methods


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


@pytest.mark.django_db
def test_tasks():

    ticket = TicketFactory()
    t1 = TaskFactory(ticket=ticket, title='t1')
    t2 = TaskFactory(ticket=ticket, title='t2', complete=timezone.now())
    t3 = TaskFactory(ticket=ticket, title='t3')
    assert ['t1', 't3'] == [t.title for t in ticket.tasks()]
