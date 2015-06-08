# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from crm.tests.factories import (
    ContactFactory,
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
    ticket = TicketFactory(
        contact=ContactFactory(name='Patrick'),
        priority=PriorityFactory(name='High'),
        title='Mow the lawn',
        user_assigned=UserFactory(username='pkimber'),
    )
    # get
    response = api_client.get(reverse('api.crm.ticket'))
    assert status.HTTP_200_OK == response.status_code
    assert [
        {
            'contact': 'Patrick',
            'due': None,
            'id': ticket.pk,
            'priority': 'High',
            'title': 'Mow the lawn',
            'user_assigned': 'pkimber',
        },
    ] == response.data
