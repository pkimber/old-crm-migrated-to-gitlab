import pytest

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from .factories import TicketFactory


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_task_create(self):
        ticket = TicketFactory()
        url = reverse('crm.task.create', kwargs={'pk': ticket.pk})
        self.assert_staff_only(url)
