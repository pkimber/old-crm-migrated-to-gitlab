"""Simple tests to make sure a view doesn't throw any exceptions"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
    make_user_contact,
)
from login.tests.model_maker import make_user


class TestView(TestCase):

    def setUp(self):
        """tom has access to contact icl"""
        tom = make_user('tom')
        self.icl = make_contact('icl', 'ICL')
        make_user_contact(tom, self.icl)
        self.sew = make_ticket(
            self.icl, tom, 'Sew', 'Sewing', make_priority('Low', 1)
        )
        # tom should not have access to aec
        make_contact('aec', 'AEC')
        self.client.login(
            username=tom.username, password=tom.username
        )

    def test_home(self):
        url = reverse('crm.home')
        self._assert_get(url)

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.icl.slug})
        self._assert_get(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def test_ticket_edit(self):
        url = reverse('crm.ticket.update', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def _assert_get(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
