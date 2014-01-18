from datetime import datetime
from datetime import timedelta

from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_note_fence_forgot,
)
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)
from search.tests.helper import check_search_methods


class TestNote(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        contact_contractor()
        self.note = get_note_fence_forgot()

    def test_search_methods(self):
        check_search_methods(self.note)

    def test_str(self):
        str(self.note)

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
