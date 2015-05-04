# -*- encoding: utf-8 -*-
from datetime import date

from django.test import TestCase

from search.tests.helper import check_search_methods

from crm.tests.factories import TicketFactory


class TestContact(TestCase):

    def test_due(self):
        ticket = TicketFactory(due=date.today())
        assert not ticket.is_overdue

    def test_overdue(self):
        ticket = TicketFactory(due=date(2010, 1, 1))
        assert ticket.is_overdue

    def test_search_methods(self):
        check_search_methods(TicketFactory())

    def test_str(self):
        str(TicketFactory())
