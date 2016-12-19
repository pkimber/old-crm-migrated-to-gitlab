# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase

from contact.tests.factories import ContactFactory, UserContactFactory
from crm.tests.factories import CrmContactFactory, TicketFactory
from login.tests.factories import TEST_PASSWORD, UserFactory
from login.tests.fixture import perm_check
from login.tests.scenario import get_user_web


@pytest.mark.django_db
def test_contact_detail(perm_check):
    UserContactFactory(user=get_user_web())
    contact = ContactFactory()
    crm_contact = CrmContactFactory(contact=contact)
    url = reverse('contact.detail', args=[contact.pk])
    perm_check.staff(url)
