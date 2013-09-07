from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
)
from login.tests.model_maker import make_user


class TestViewPerm(TestCase):
    """user 'tom' should not be able to view the 'aec' contact"""

    def setUp(self):
        """tom has access to contact icl"""
        self.sam = make_user('sam', is_staff=True)
        self.tom = make_user('tom')
        self.client.login(
            username=self.tom.username, password=self.tom.username
        )
        # tom should not have access to aec
        self.zed = make_user('zed')
        self.aec = make_contact('aec', 'AEC')
        self.dig = make_ticket(
            self.aec, self.zed, 'Dig', make_priority('High', 1)
        )
        self.note = make_note(
            self.dig, self.zed, 'Plant some carrots and some peas'
        )

    def test_contact_create(self):
        url = reverse('crm.contact.create')
        self._assert_staff_only(url)

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.aec.slug})
        self._assert_perm_denied(url)

    def test_contact_list(self):
        url = reverse('crm.contact.list')
        self._assert_staff_only(url)

    def test_contact_update(self):
        url = reverse('crm.contact.update', kwargs={'slug': self.aec.slug})
        self._assert_staff_only(url)

    def test_note_create(self):
        url = reverse('crm.note.create', kwargs={'pk': self.dig.pk})
        self._assert_perm_denied(url)

    def test_note_update(self):
        url = reverse('crm.note.update', kwargs={'pk': self.note.pk})
        self._assert_perm_denied(url)

    def test_ticket_create(self):
        url = reverse('crm.ticket.create', kwargs={'slug': self.aec.slug})
        self._assert_perm_denied(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.dig.pk})
        self._assert_perm_denied(url)

    def test_ticket_home(self):
        url = reverse('crm.ticket.home')
        response = self.client.get(url)
        ticket_list = response.context['ticket_list']
        contact_slugs = [item.contact.slug for item in ticket_list]
        self.assertNotIn(
            self.aec.slug,
            contact_slugs,
            "user '{}' should not have access to contact '{}'".format(
                self.tom.username, self.aec.slug
            )
        )

    def test_ticket_update(self):
        url = reverse('crm.ticket.update', kwargs={'pk': self.dig.pk})
        self._assert_perm_denied(url)

    def _assert_perm_denied(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )

    def _assert_staff_only(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )
        self.client.login(
            username=self.sam.username, password=self.sam.username
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "status {}: staff user '{}' should have access "
            "to this url: '{}'".format(
                response.status_code, self.sam.username, url
            )
        )
