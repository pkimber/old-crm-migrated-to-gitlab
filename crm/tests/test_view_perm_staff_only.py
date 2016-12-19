# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase

from contact.tests.factories import ContactFactory
from crm.tests.factories import CrmContactFactory, TicketFactory
from login.tests.fixture import perm_check
from login.tests.factories import TEST_PASSWORD


@pytest.mark.django_db
def test_contact_update(perm_check):
    contact = ContactFactory()
    crm_contact = CrmContactFactory(contact=contact)
    url = reverse('crm.contact.update', args=[crm_contact.pk])
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
def test_ticket_child_create(perm_check):
    ticket = TicketFactory()
    url = reverse('crm.ticket.child.create', kwargs={'pk': ticket.pk})
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
