# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Initialise crm application"

    def handle(self, *args, **options):
        print("Initialised 'crm' app...")
