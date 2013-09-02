from django.core.management.base import BaseCommand

from crm.tests.model_maker import make_contact
from login.tests.model_maker import make_user


class Command(BaseCommand):

    help = "Create demo data for 'crm'"

    def handle(self, *args, **options):
        fred = make_user('fred')
        matt = make_user('matt')
        contact = make_contact(
            'pkimber',
            'Patrick Kimber',
            address='High Street\nExeter\nDevon',
            mail='mail@pkimber.net',
            url='https://pkimber.net',
            phone='01837 123 456',
            postcode='EX2 3DE'
        )
        contact.users.add(fred)
        contact.users.add(matt)
        make_contact(
            'ssmith',
            'Sam Smith',
        )
        print("Created 'crm' demo data...")
