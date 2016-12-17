# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from crm.tests.factories import CrmContactFactory, NoteFactory, TicketFactory
from login.tests.factories import TEST_PASSWORD
from login.tests.fixture import perm_check
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


@pytest.mark.django_db
def test_crm_contact_create(perm_check):
    contact = ContactFactory()
    url = reverse(
        'crm.contact.create',
        kwargs={'slug': contact.user.username}
    )
    perm_check.staff(url)


@pytest.mark.django_db
def test_crm_contact_update(perm_check):
    contact = ContactFactory()
    CrmContactFactory(contact=contact)
    url = reverse(
        'crm.contact.update',
        kwargs={'slug': contact.user.username}
    )
    perm_check.staff(url)


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
    url = reverse('crm.ticket.create', kwargs={'slug': contact.user.username})
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
