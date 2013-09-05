from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
)
from login.tests.model_maker import make_user


class TestViewPerm(TestCase):

    def setUp(self):
        """tom has access to contact icl"""
        self.tom = make_user('tom')
        self.client.login(
            username=self.tom.username, password=self.tom.username
        )
        # tom should not have access to aec
        self.zed = make_user('zed')
        self.aec = make_contact('aec', 'AEC')
        self.dig = make_ticket(
            self.aec, self.zed, 'Dig', 'Dig garden', make_priority('High', 1)
        )

    def test_home(self):
        url = reverse('crm.home')
        response = self.client.get(url)
        ticket_list = response.context['ticket_list']
        contact_slugs = [item.contact.slug for item in ticket_list]
        self.assertNotIn(
            self.aec.slug,
            contact_slugs,
            "user '{}' should not have access to contact '{}'".format(
                self.tom.username, self.aec.slug
            )
        )

    def test_contact_detail(self):
        """
        user 'tom' should not be able to view tickets for the 'aec' contact
        """
        url = reverse('crm.contact.detail', kwargs={'slug': self.aec.slug})
        self._assert_perm_denied(url)

    def test_ticket_detail(self):
        """
        user 'tom' should not be able to view tickets for the 'aec' contact
        """
        url = reverse('crm.ticket.detail', kwargs={'pk': self.dig.pk})
        self._assert_perm_denied(url)

    def _assert_perm_denied(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )
