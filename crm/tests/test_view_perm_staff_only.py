from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
    get_ticket_fence_for_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_fred,
    get_user_staff,
    user_contractor,
)


class TestViewPermStaffOnly(TestCase):
    """
    Fred is a farmer who has a ticket for fencing the orchard.  There is a note
    attached to this ticket to say we forgot to order the fence posts.

    Fred shouldn't have access to the following views even though the data
    belongs to him.

    Only a member of staff should be able to access the following views.
    """

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        self.farm = get_contact_farm()
        self.fence = get_ticket_fence_for_farm()
        self.fred = get_user_fred()
        self.client.login(
            username=self.fred.username, password=self.fred.username
        )

    def test_contact_create(self):
        url = reverse('crm.contact.create')
        self._assert_staff_only(url)

    def test_contact_list(self):
        url = reverse('crm.contact.list')
        self._assert_staff_only(url)

    def test_contact_update(self):
        url = reverse('crm.contact.update', kwargs={'slug': self.farm.slug})
        self._assert_staff_only(url)

    def test_ticket_complete(self):
        url = reverse('crm.ticket.complete', kwargs={'pk': self.fence.pk})
        self._assert_staff_only(url)

    def test_ticket_list(self):
        url = reverse('crm.ticket.list')
        self._assert_staff_only(url)

    def _assert_staff_only(self, url):
        staff = get_user_staff()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.fred.username, url
            )
        )
        self.client.login(
            username=staff.username, password=staff.username
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "status {}: staff user '{}' should have access "
            "to this url: '{}'".format(
                response.status_code, staff.username, url
            )
        )
