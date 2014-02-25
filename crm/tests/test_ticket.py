# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase

from search.tests.helper import check_search_methods

from crm.tests.model_maker import (
    make_contact,
    make_ticket,
    make_priority,
)
from login.tests.scenario import make_user


class TestContact(TestCase):

    def setUp(self):
        contact = make_contact('Patrick', 'Kimber')
        user = make_user('Andrea')
        self.ticket = make_ticket(
            contact,
            user,
            'Cook a pizza',
            make_priority('High', 1),
        )

    def test_search_methods(self):
        check_search_methods(self.ticket)

    def test_str(self):
        str(self.ticket)
