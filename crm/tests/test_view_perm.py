from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_contact_farm,
    get_note_fence_forgot,
    get_ticket_fence,
)
from login.tests.scenario import (
    get_user_fred,
    get_user_sara,
    get_user_staff,
    user_contractor,
    user_default,
)


class TestViewPerm(TestCase):
    """user 'tom' should not be able to view the 'aec' contact"""

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
        self.farm = get_contact_farm()
        self.fence = get_ticket_fence()
        self.note = get_note_fence_forgot()
        self.sara = get_user_sara()
        self.client.login(
            username=self.sara.username, password=self.sara.username
        )

    def test_contact_create(self):
        url = reverse('crm.contact.create')
        self._assert_staff_only(url)

    def test_contact_detail(self):
        url = reverse('crm.contact.detail', kwargs={'slug': self.farm.slug})
        self._assert_perm_denied(url)

    def test_contact_list(self):
        url = reverse('crm.contact.list')
        self._assert_staff_only(url)

    def test_contact_update(self):
        url = reverse('crm.contact.update', kwargs={'slug': self.farm.slug})
        self._assert_staff_only(url)

    def test_note_create(self):
        url = reverse('crm.note.create', kwargs={'pk': self.fence.pk})
        self._assert_perm_denied(url)

    def test_note_update(self):
        url = reverse('crm.note.update', kwargs={'pk': self.note.pk})
        self._assert_perm_denied(url)

    def test_ticket_complete(self):
        url = reverse('crm.ticket.complete', kwargs={'pk': self.fence.pk})
        self._assert_staff_only(url)

    def test_ticket_create(self):
        url = reverse('crm.ticket.create', kwargs={'slug': self.farm.slug})
        self._assert_perm_denied(url)

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.fence.pk})
        self._assert_perm_denied(url)

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

    def _assert_staff_only(self, url):
        fred = get_user_fred()
        staff = get_user_staff()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, fred.username, url
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
