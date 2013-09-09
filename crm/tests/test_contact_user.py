from django.db import IntegrityError
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_user_contact,
)
from crm.tests.scenario import (
    contact_contractor,
)
from login.tests.scenario import (
    get_fred,
    get_sara,
    user_contractor,
)


class TestContactUser(TestCase):

    def test_link_user_to_contact(self):
        """Create a contact and link it to a user"""
        user_contractor()
        contact_contractor()
        user_contacts = get_fred().usercontact_set.all()
        self.assertIn("Fred's Farm", user_contacts[0].contact.name)

    def test_one_contact_per_user(self):
        """Make sure a user can only link to one contact"""
        user_contractor()
        contact_contractor()
        self.assertRaises(
            IntegrityError,
            make_user_contact,
            get_sara(),
            make_contact('zoo', 'Bristol Zoo')
        )
