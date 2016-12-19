# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from crm.tests.factories import CrmContactFactory, IndustryFactory
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_get_absolute_url():
    contact = ContactFactory(user=UserFactory(username='alan'))
    obj = CrmContactFactory(contact=contact)
    expect = reverse('contact.detail', args=[contact.pk])
    assert expect == obj.get_absolute_url()


@pytest.mark.django_db
def test_str():
    user = UserFactory(first_name='Alan', last_name='Jones')
    contact = ContactFactory(user=user)
    industry = IndustryFactory(name='Agri')
    obj = CrmContactFactory(contact=contact, industry=industry)
    assert 'Alan Jones: Agri' == str(obj)


@pytest.mark.django_db
def test_str_no_hourly_rate():
    user = UserFactory(first_name='Alan', last_name='Jones')
    contact = ContactFactory(user=user)
    obj = CrmContactFactory(contact=contact, industry=None)
    assert 'Alan Jones' == str(obj)
