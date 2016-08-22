# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase

from contact.tests.factories import ContactFactory
from crm.tests.factories import CrmContactFactory, TicketFactory
from login.tests.fixture import perm_check
from login.tests.factories import TEST_PASSWORD


# class TestViewPermStaffOnly(TestCase):
#     """
#     Fred is a farmer who has a ticket for fencing the orchard.  There is a note
#     attached to this ticket to say we forgot to order the fence posts.
#
#     Fred shouldn't have access to the following views even though the data
#     belongs to him.
#
#     Only a member of staff should be able to access the following views.
#     """
#
#     def setUp(self):
#         user_contractor()
#         default_scenario_login()
#         default_scenario_crm()
#         self.farm = get_contact_farm()
#         self.fence = get_ticket_fence_for_farm()
#         self.fred = get_user_fred()
#         self.assertTrue(self.client.login(
#             username=self.fred.username, password=TEST_PASSWORD
#         ))


# @pytest.mark.django_db
# def test_contact_create(perm_check):
#     url = reverse('crm.contact.create')
#     perm_check.staff(url)
#
#
# @pytest.mark.django_db
# def test_contact_list(perm_check):
#     url = reverse('crm.contact.list')
#     perm_check.staff(url)
#
#
# @pytest.mark.django_db
# def test_contact_update(perm_check):
#     url = reverse('crm.contact.update', kwargs={'slug': self.farm.slug})
#     perm_check.staff(url)


@pytest.mark.django_db
def test_contact_update(perm_check):
    contact = ContactFactory()
    crm_contact = CrmContactFactory(contact=contact)
    url = reverse('crm.contact.update', args=[contact.user.username])
    print(url)
    perm_check.staff(url)


@pytest.mark.django_db
def test_project_ticket_due_list(perm_check):
    url = reverse('crm.project.ticket.due.list')
    perm_check.staff(url)


@pytest.mark.django_db
def test_project_ticket_priority_list(perm_check):
    url = reverse('crm.project.ticket.priority.list')
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_complete(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.complete', kwargs={'pk': ticket.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_list(perm_check):
    url = reverse('crm.ticket.list')
    perm_check.staff(url)
