from django.contrib.auth.models import User
from django.test import TestCase

from crm.tests.model_maker import make_contact
from login.tests.model_maker import make_user


class TestContactUser(TestCase):

    def test_link_user_to_contact(self):
        """Create a contact and link it to a user"""
        contact = make_contact('pkimber', 'Patrick Kimber')
        contact.users.add(make_user('fred'))
        user = User.objects.get(username='fred')
        contacts = user.contact_set.all()
        self.assertIn('Kimber', contacts[0].name)
