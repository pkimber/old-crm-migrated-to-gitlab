# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal
from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from crm.models import CrmContact, Ticket
from crm.tests.factories import (
    CrmContactFactory,
    IndustryFactory,
    PriorityFactory,
    TicketFactory,
)
from invoice.models import TimeRecord
from invoice.tests.factories import QuickTimeRecordFactory
from login.tests.factories import TEST_PASSWORD, UserFactory


@pytest.mark.django_db
def test_crm_contact_create(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    url = reverse(
        'crm.contact.create',
        kwargs={'pk': contact.pk}
    )
    data = {
        'industry': IndustryFactory(name='Agriculture').pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.pk])
    assert expect == response['Location']
    crm_contact = CrmContact.objects.get(contact=contact)
    assert 'Agriculture' == crm_contact.industry.name


@pytest.mark.django_db
def test_crm_contact_update(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    crm_contact = CrmContactFactory(contact=contact)
    url = reverse(
        'crm.contact.update',
        kwargs={'pk': crm_contact.pk}
    )
    data = {
        'industry': IndustryFactory(name='Agriculture').pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.pk])
    assert expect == response['Location']
    crm_contact = CrmContact.objects.get(contact=contact)
    assert 'Agriculture' == crm_contact.industry.name


@pytest.mark.django_db
def test_ticket_detail(client):
    user = UserFactory(username='staff', is_staff=True)
    quick = QuickTimeRecordFactory(user=user)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    ticket = TicketFactory()
    url = reverse('crm.ticket.detail', kwargs={'pk': ticket.pk})
    data = {
        'quick': quick.pk,
    }
    assert 0 == TimeRecord.objects.count()
    response = client.post(url, data)
    assert 302 == response.status_code
    assert url == response['Location']
    assert 1 == TimeRecord.objects.count()
    time_record = TimeRecord.objects.first()
    assert quick.time_code.description == time_record.time_code.description


@pytest.mark.django_db
def test_ticket_create(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    priority = PriorityFactory()
    url = reverse('crm.ticket.create', kwargs={'pk': contact.pk})
    data = {
        'fixed_price': True,
        'priority': priority.pk,
        'title': 'Apple Juice',
    }
    response = client.post(url, data)
    assert 302 == response.status_code, response.context['form'].errors
    ticket = Ticket.objects.get(contact=contact)
    expect = reverse('crm.ticket.detail', args=[ticket.pk])
    assert expect == response['Location']
    assert ticket.fixed_price is True
    assert priority.pk == ticket.priority.pk
    assert 'Apple Juice' == ticket.title


@pytest.mark.django_db
def test_ticket_update(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    priority = PriorityFactory()
    ticket = TicketFactory()
    assert ticket.fixed_price is False
    url = reverse('crm.ticket.update', kwargs={'pk': ticket.pk})
    data = {
        'fixed_price': True,
        'priority': priority.pk,
        'title': 'Apple Juice',
    }
    response = client.post(url, data)
    assert 302 == response.status_code, response.context['form'].errors
    expect = reverse('crm.ticket.detail', args=[ticket.pk])
    assert expect == response['Location']
    ticket.refresh_from_db()
    assert ticket.fixed_price is True
    assert priority.pk == ticket.priority.pk
    assert 'Apple Juice' == ticket.title
