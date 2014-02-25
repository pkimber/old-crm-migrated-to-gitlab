# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from crm.tests.scenario import default_scenario_crm


class Command(BaseCommand):

    help = "Create demo data for 'crm'"

    def handle(self, *args, **options):
        default_scenario_crm()
        print("Created 'crm' demo data...")
