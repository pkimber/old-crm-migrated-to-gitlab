from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_contact_farm,
    get_note_fence_forgot,
    get_ticket_fence_for_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_sara,
    user_contractor,
)


class TestViewPermUser(TestCase):
    """
    fred is a farmer who has a ticket for fencing the orchard.  There is a note
    attached to this ticket to say we forgot to order the fence posts.

    sara is a smallholder who shouldn't be able to see any of fred's
    information when she is logged into the system
    """

    def setUp(self):
        user_contractor()
        default_scenario_login()
        contact_contractor()
        self.farm = get_contact_farm()
        self.fence = get_ticket_fence_for_farm()
        self.note = get_note_fence_forgot()
        self.sara = get_user_sara()
        self.client.login(
            username=self.sara.username, password=self.sara.username
        )

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.farm.slug})
        self._assert_perm_denied(url)

    def test_note_create(self):
        url = reverse('crm.note.create', kwargs={'pk': self.fence.pk})
        self._assert_perm_denied(url)

    def test_note_update(self):
        url = reverse('crm.note.update', kwargs={'pk': self.note.pk})
        self._assert_perm_denied(url)

    def test_ticket_create(self):
        url = reverse('crm.ticket.create', kwargs={'slug': self.farm.slug})
        self._assert_perm_denied(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.fence.pk})
        self._assert_perm_denied(url)

    def test_ticket_update(self):
        url = reverse('crm.ticket.update', kwargs={'pk': self.fence.pk})
        self._assert_perm_denied(url)

    def _assert_perm_denied(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.sara.username, url
            )
        )
