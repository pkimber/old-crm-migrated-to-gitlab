# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from crm.tests.factories import (
    NoteFactory,
    TicketFactory,
)
from login.tests.fixture import perm_check


# class TestViewPermUser(TestCase):
#     """
#     fred is a farmer who has a ticket for fencing the orchard.  There is a note
#     attached to this ticket to say we forgot to order the fence posts.
#
#     sara is a smallholder who shouldn't be able to see any of fred's
#     information when she is logged into the system
#     """
#
#     def setUp(self):
#         user_contractor()
#         default_scenario_login()
#         default_scenario_crm()
#         self.farm = get_contact_farm()
#         self.fence = get_ticket_fence_for_farm()
#         self.note = get_note_fence_forgot()
#         self.sara = get_user_sara()
#         self.assertTrue(self.client.login(
#             username=self.sara.username, password=TEST_PASSWORD
#         ))

# def test_contact_detail(self):
#     url = reverse('contact.detail', kwargs={'slug': self.farm.slug})
#     self._assert_perm_denied(url)

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
def test_ticket_create(perm_check):
    contact = ContactFactory()
    url = reverse(
        'crm.ticket.create',
        kwargs={'pk': contact.pk}
    )
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_detail(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.detail', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_update(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.update', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


#def _assert_perm_denied(self, url):
#    response = self.client.get(url)
#    self.assertEqual(
#        response.status_code,
#        403,
#        "status {}: user '{}' should not have access "
#        "to this url: '{}'".format(
#            response.status_code, self.sara.username, url
#        )
#    )
