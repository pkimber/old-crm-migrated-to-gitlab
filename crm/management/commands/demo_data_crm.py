from django.core.management.base import BaseCommand

from crm.tests.model_maker import make_contact


class Command(BaseCommand):

    help = "Create demo data for 'crm'"

    def handle(self, *args, **options):
        make_contact(
            'pkimber',
            'Patrick Kimber',
            address='High Street\nExeter\nDevon',
            postcode='EX2 3DE'
        )
        make_contact('smith', 'John Smith')
        print("Created 'crm' demo data...")
