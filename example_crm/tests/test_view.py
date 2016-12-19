# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from crm.tests.factories import CrmContactFactory
from contact.tests.factories import UserContactFactory
from invoice.tests.factories import InvoiceContactFactory
from login.tests.fixture import perm_check
from login.tests.scenario import get_user_web


@pytest.mark.django_db
def test_contact_detail(perm_check):
    UserContactFactory(user=get_user_web())
    user_contact = UserContactFactory()
    InvoiceContactFactory(contact=user_contact.contact)
    UserContactFactory(contact=user_contact.contact)
    url = reverse('contact.detail', args=[user_contact.contact.pk])
    perm_check.staff(url)
