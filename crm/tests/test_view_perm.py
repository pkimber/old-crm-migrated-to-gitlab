from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
    make_user_contact,
)
from login.tests.model_maker import make_user


class TestViewPerm(TestCase):

    def setUp(self):
        """tom has access to contact icl"""
        self.tom = make_user('tom')
        self.icl = make_contact('icl', 'ICL')
        make_user_contact(self.tom, self.icl)
        self.sew = make_ticket(
            self.icl, self.tom, 'Sew', 'Sewing', make_priority('Low', 1)
        )
        self.note = make_note(
            self.sew, self.tom, 'Cut out some material and make a pillow case'
        )
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

    def test_ticket_detail(self):
        url = reverse('crm.ticket.detail', kwargs={'pk': self.dig.pk})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access to tickets "
            "for contact '{}'".format(
                response.status_code, self.tom.username, self.dig.contact.slug
            )
        )
