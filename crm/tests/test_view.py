# -*- encoding: utf-8 -*-
"""Simple tests to make sure a view doesn't throw any exceptions"""
import pytest

from django.core.urlresolvers import reverse

# from crm.tests.scenario import (
#     default_scenario_crm,
#     get_contact_farm,
#     get_note_fence_forgot,
#     get_ticket_fence_for_farm,
# )
from contact.tests.factories import ContactFactory
from crm.tests.factories import (
    NoteFactory,
    TicketFactory,
)
from login.tests.factories import TEST_PASSWORD
from login.tests.fixture import perm_check
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


#class TestView(TestCase):
#    """Make sure a staff user can access all the standard screens"""
#
#    def setUp(self):
#        user_contractor()
#        default_scenario_login()
#        default_scenario_crm()
#        self.contact = get_contact_farm()
#        self.staff = get_user_staff()
#        self.note = get_note_fence_forgot()
#        self.ticket = get_ticket_fence_for_farm()


@pytest.mark.django_db
def test_note_create(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.note.create', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_note_update(perm_check):
    note = NoteFactory()
    url = reverse('crm.note.update', kwargs={'pk': note.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_complete(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.complete', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_create(perm_check):
    contact = ContactFactory()
    url = reverse('crm.ticket.create', kwargs={'slug': contact.slug})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_detail(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.detail', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_home(perm_check):
    TicketFactory()
    url = reverse('crm.ticket.home')
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_update(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.update', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


# def _assert_get(self, url):
#     # User must be logged in to access this URL
#     response = self.client.get(url)
#     self.assertEqual(
#         response.status_code,
#         302,
#         'status {}\n{}'.format(response.status_code, response),
#     )
#     # Log the user in so they can access this URL
#     self.client.login(
#         username=self.staff.username,
#         password=TEST_PASSWORD,
#     )
#     response = self.client.get(url)
#     self.assertEqual(
#         response.status_code,
#         200,
#         'status {}\n{}'.format(response.status_code, response),
#     )
