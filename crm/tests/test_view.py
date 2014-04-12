# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

"""Simple tests to make sure a view doesn't throw any exceptions"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
    get_note_fence_forgot,
    get_ticket_fence_for_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


class TestView(TestCase):
    """Make sure a staff user can access all the standard screens"""

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        self.contact = get_contact_farm()
        self.staff = get_user_staff()
        self.note = get_note_fence_forgot()
        self.ticket = get_ticket_fence_for_farm()

    def test_contact_create(self):
        url = reverse('crm.contact.create')
        self._assert_get(url)

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.contact.slug})
        self._assert_get(url)

    def test_contact_list(self):
        url = reverse('crm.contact.list')
        self._assert_get(url)

    def test_contact_update(self):
        url = reverse('crm.contact.update', kwargs={'slug': self.contact.slug})
        self._assert_get(url)

    def test_note_create(self):
        url = reverse('crm.note.create', kwargs={'pk': self.ticket.pk})
        self._assert_get(url)

    def test_note_update(self):
        url = reverse('crm.note.update', kwargs={'pk': self.note.pk})
        self._assert_get(url)

    def test_ticket_complete(self):
        url = reverse('crm.ticket.complete', kwargs={'pk': self.ticket.pk})
        self._assert_get(url)

    def test_ticket_create(self):
        url = reverse('crm.ticket.create', kwargs={'slug': self.contact.slug})
        self._assert_get(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.ticket.pk})
        self._assert_get(url)

    def test_ticket_home(self):
        url = reverse('crm.ticket.home')
        self._assert_get(url)

    def test_ticket_update(self):
        url = reverse('crm.ticket.update', kwargs={'pk': self.ticket.pk})
        self._assert_get(url)

    def _assert_get(self, url):
        # User must be logged in to access this URL
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            'status {}\n{}'.format(response.status_code, response),
        )
        # Log the user in so they can access this URL
        self.client.login(
            username=self.staff.username,
            password=self.staff.username,
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            'status {}\n{}'.format(response.status_code, response),
        )
