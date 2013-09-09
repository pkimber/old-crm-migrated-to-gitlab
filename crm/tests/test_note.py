from datetime import datetime
from datetime import timedelta

from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_note_fence_forgot,
)
from login.tests.scenario import (
    user_contractor,
    user_default,
)


class TestNote(TestCase):

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
        self.note = get_note_fence_forgot()

    def test_modified_today(self):
        self.assertTrue(self.note.modified_today())

    def test_modified_tomorrow(self):
        tomorrow = datetime.today() + timedelta(days=1)
        self.note.created = tomorrow
        self.note.save()
        self.assertFalse(self.note.modified_today())

    def test_modified_yesterday(self):
        yesterday = datetime.today() - timedelta(days=1)
        self.note.created = yesterday
        self.note.save()
        self.assertFalse(self.note.modified_today())
