# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_sara,
    user_contractor,
)


class TestViewPermHome(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        self.farm = get_contact_farm()
        self.sara = get_user_sara()
        self.client.login(
            username=self.sara.username, password=self.sara.username
        )

    def test_ticket_home(self):
        url = reverse('crm.ticket.home')
        response = self.client.get(url)
        ticket_list = response.context['ticket_list']
        contact_slugs = [item.contact.slug for item in ticket_list]
        self.assertNotIn(
            self.farm.slug,
            contact_slugs,
            "user '{}' should not have access to contact '{}'".format(
                self.sara.username, self.farm.slug
            )
        )
