"""Simple tests to make sure a view doesn't throw any exceptions"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
    make_user_contact,
)
from login.tests.model_maker import make_user


class TestView(TestCase):

    def setUp(self):
        """tom has access to contact icl"""
        self.tom = make_user('tom')
        self.icl = make_contact('icl', 'ICL')
        make_user_contact(self.tom, self.icl)
        self.sew = make_ticket(
            self.icl, self.tom, 'Sew', 'Sewing', make_priority('Low', 1)
        )
        self.note = make_note(
            self.sew, self.tom, 'Cut out some material and make a pillow case'
        )

    def test_home(self):
        url = reverse('crm.home')
        self._assert_get(url)

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.icl.slug})
        self._assert_get(url)

    def test_note_create(self):
        url = reverse('crm.note.create', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def test_note_update(self):
        url = reverse('crm.note.update', kwargs={'pk': self.note.pk})
        self._assert_get(url)

    def test_ticket_create(self):
        url = reverse('crm.ticket.create', kwargs={'slug': self.icl.slug})
        self._assert_get(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def test_ticket_update(self):
        url = reverse('crm.ticket.update', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def _assert_get(self, url):
        # User must be logged in to access this URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302, response)
        # Log the user in so they can access this URL
        self.client.login(
            username=self.tom.username, password=self.tom.username
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response)
