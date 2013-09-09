from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from crm.tests.model_maker import (
    make_contact,
    make_industry,
    make_note,
    make_priority,
    make_ticket,
    make_user_contact,
)
from crm.tests.scenario import (
    contact_contractor,
)
from login.tests.model_maker import make_user


class Command(BaseCommand):

    help = "Create demo data for 'crm'"

    def handle(self, *args, **options):
        contact_contractor()
        print("Created 'crm' demo data...")

    def old_code_no_longer_used(self):
        fred = make_user('fred')
        matt = make_user('matt')
        pkimber = make_contact(
            'pkimber',
            'Patrick Kimber',
            address='High Street\nExeter\nDevon',
            mail='mail@pkimber.net',
            url='https://pkimber.net',
            phone='01837 123 456',
            hourly_rate=Decimal('10.00'),
            industry=make_industry('Farming'),
        )
        make_user_contact(fred, pkimber)
        description = """Hey diddle diddle rhyme
Hey diddle diddle, the cat and the fiddle,
The cow jumped over the moon.
The little dog laughed to see such fun
And the dish ran away with the spoon!
        """
        ticket = make_ticket(
            pkimber,
            matt,
            "Milk the cows",
            make_priority('High', 1),
            description=description,
            due=datetime.today(),
        )
        make_note(ticket, fred, "Finished the milking")
        make_note(ticket, matt, "Cows eating silage")
        ticket = make_ticket(
            pkimber,
            fred,
            "Feed the pigs",
            make_priority('Medium', 2),
        )
        ssmith = make_contact(
            'ssmith',
            'Sam Smith',
            hourly_rate=Decimal('20.00'),
            industry=make_industry('Leisure'),
        )
        ticket = make_ticket(
            ssmith,
            fred,
            "Move the electric fence",
            make_priority('Low', 2),
        )
        print("Created 'crm' demo data...")
