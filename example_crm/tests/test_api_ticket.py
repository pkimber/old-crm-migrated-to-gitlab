# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from contact.tests.factories import ContactFactory
from crm.tests.factories import (
    #CrmContactFactory,
    PriorityFactory,
    TicketFactory,
)
from login.tests.factories import UserFactory


@pytest.yield_fixture
def api_client():
    """Create an admin user, and login using the token."""
    user = UserFactory(username='staff', is_staff=True)
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
    yield client


@pytest.mark.django_db
def test_api_ticket(api_client):
    user = UserFactory(first_name='Andrea', username='andrea')
    t1 = TicketFactory(
        contact=ContactFactory(company_name='', user=user),
        priority=PriorityFactory(name='Medium'),
        title='Mow the lawn',
        user_assigned=UserFactory(username='akimber'),
    )
    user = UserFactory(first_name='Patrick', username='patrick')
    t2 = TicketFactory(
        contact=ContactFactory(company_name='', user=user),
        priority=PriorityFactory(name='High'),
        title='Make a cup of tea',
        user_assigned=UserFactory(username='pkimber'),
    )
    # get
    response = api_client.get(reverse('api.crm.ticket'))
    assert status.HTTP_200_OK == response.status_code
    assert [
        {
            'contact': 'andrea',
            'due': None,
            'id': t1.pk,
            'priority': 'Medium',
            'title': 'Mow the lawn',
            'username': 'akimber',
        },
        {
            'contact': 'patrick',
            'due': None,
            'id': t2.pk,
            'priority': 'High',
            'title': 'Make a cup of tea',
            'username': 'pkimber',
        },
    ] == response.data
