# -*- encoding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand

from tasklib.task import TaskWarrior

from crm.models import (
    TicketTaskWarrior,
    Ticket,
)


class Command(BaseCommand):

    help = "Update TaskWarrior"

    def handle(self, *args, **options):
        data_location = settings.TASKWARRIOR
        print(settings.TASKWARRIOR)
        tw = TaskWarrior(data_location)
        tasks = tw.tasks.pending()
        for task in tasks:
            print(task['uuid'])
            print(task)
        uuid = '5de8e3bf-c2af-4455-a0b4-d61effeba82d'
        task = tw.tasks.get(uuid=uuid)
        print()
        print('task: {}'.format(task))
        ticket = Ticket.objects.get(pk=38)
        print('ticket: {}'.format(ticket))
        try:
            ticket_task = TicketTaskWarrior.objects.get(uuid=uuid)
            print('found: {}'.format(ticket_task))
            print('     : {}'.format(ticket_task.uuid))
        except TicketTaskWarrior.DoesNotExist:
            ticket_task = TicketTaskWarrior.objects.create_taskwarrior(
                uuid=task['uuid'],
                ticket=ticket,
            )
            print('create: {}'.format(ticket_task))
        print("TaskWarrior updated...")
