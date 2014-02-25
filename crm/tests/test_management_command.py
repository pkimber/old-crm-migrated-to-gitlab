# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase

from crm.management.commands import demo_data_crm
from crm.management.commands import init_app_crm
from login.management.commands import demo_data_login


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        pre_command = demo_data_login.Command()
        pre_command.handle()
        command = demo_data_crm.Command()
        command.handle()

    def test_init_app(self):
        """ Test the management command """
        command = init_app_crm.Command()
        command.handle()
