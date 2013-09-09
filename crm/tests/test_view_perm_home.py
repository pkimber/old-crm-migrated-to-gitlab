from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_contact_farm,
)
from login.tests.scenario import (
    get_user_sara,
    user_contractor,
    user_default,
)


class TestViewPermHome(TestCase):

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
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