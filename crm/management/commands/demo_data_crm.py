from django.core.management.base import BaseCommand

from crm.tests.scenario import (
    contact_contractor,
)


class Command(BaseCommand):

    help = "Create demo data for 'crm'"

    def handle(self, *args, **options):
        contact_contractor()
        print("Created 'crm' demo data...")
