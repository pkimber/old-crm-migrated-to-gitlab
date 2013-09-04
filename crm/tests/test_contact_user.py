from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_user_contact,
)
from login.tests.model_maker import make_user


class TestContactUser(TestCase):

    def test_link_user_to_contact(self):
        """Create a contact and link it to a user"""
        contact = make_contact(
            'pkimber',
            'Patrick Kimber',
        )
        make_user_contact(make_user('fred'), contact)
        user = User.objects.get(username='fred')
        user_contacts = user.usercontact_set.all()
        self.assertIn('Kimber', user_contacts[0].contact.name)

    def test_one_contact_per_user(self):
        """Make sure a user can only link to one contact"""
        fred = make_user('fred')
        jsmith = make_contact('jsmith', 'John Smith')
        pkimber = make_contact('pkimber', 'Patrick Kimber')
        make_user_contact(fred, pkimber)
        self.assertRaises(
            IntegrityError,
            make_user_contact,
            fred,
            jsmith,
        )
