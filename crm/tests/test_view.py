# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal
from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from crm.models import CrmContact
from crm.tests.factories import CrmContactFactory, IndustryFactory
from login.tests.factories import TEST_PASSWORD, UserFactory


@pytest.mark.django_db
def test_crm_contact_create(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    url = reverse(
        'crm.contact.create',
        kwargs={'slug': contact.user.username}
    )
    data = {
        'industry': IndustryFactory(name='Agriculture').pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.user.username])
    assert expect == response['Location']
    crm_contact = CrmContact.objects.get(contact=contact)
    assert 'Agriculture' == crm_contact.industry.name


@pytest.mark.django_db
def test_crm_contact_update(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    CrmContactFactory(contact=contact)
    url = reverse(
        'crm.contact.update',
        kwargs={'slug': contact.user.username}
    )
    data = {
        'industry': IndustryFactory(name='Agriculture').pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.user.username])
    assert expect == response['Location']
    crm_contact = CrmContact.objects.get(contact=contact)
    assert 'Agriculture' == crm_contact.industry.name
