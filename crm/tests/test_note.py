from datetime import datetime
from datetime import timedelta

from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
)
from login.tests.model_maker import make_user


class TestNote(TestCase):

    def setUp(self):
        icl = make_contact('icl', 'ICL')
        sew = make_ticket(
            icl, make_user('tom'), 'Sew', make_priority('Low', 1)
        )
        self.note = make_note(
            sew,
            make_user('zed'),
            'Cut out some material and make a pillow case',
        )

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
