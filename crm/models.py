# -*- encoding: utf-8 -*-
from datetime import date

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

# from mptt.models import MPTTModel, TreeForeignKey
from reversion import revisions as reversion

from base.model_utils import TimeStampedModel


class Industry(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(Industry)


class CrmContact(TimeStampedModel):

    contact = models.OneToOneField(settings.CONTACT_MODEL)
    industry = models.ForeignKey(Industry, blank=True, null=True)

    class Meta:
        verbose_name = 'CRM Contact'
        verbose_name_plural = 'CRM Contacts'

    def __str__(self):
        return '{}'.format(self.contact.name)

reversion.register(CrmContact)


class Priority(models.Model):
    """Level 0 will exclude the ticket from normal reminder lists"""

    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()

    class Meta:
        ordering = ('-level', 'name',)
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(Priority)


class TicketManager(models.Manager):

    def contact(self, contact):
        return self.model.objects.filter(
            contact=contact,
        ).exclude(
            deleted=True,
        )

    def current(self):
        return self.model.objects.filter(complete__isnull=True)

    def planner(self):
        return self.model.objects.filter(
            complete__isnull=True
        ).exclude(
            priority__level=0
        )


class Ticket(models.Model): #MPTTModel):

    contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='ticket_contact')
    # parent = TreeForeignKey(
    #     'self', null=True, blank=True, related_name='children', db_index=True
    # )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    priority = models.ForeignKey(Priority)
    due = models.DateField(blank=True, null=True)
    complete = models.DateTimeField(blank=True, null=True)
    complete_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    user_assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(blank=True, null=True)
    user_deleted = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='+',
    )
    objects = TicketManager()

    class Meta:
        ordering = ('-complete', 'due', '-priority__level', 'created',)
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.pk])

    def get_summary_description(self):
        return filter(None, (
            self.title,
            self.description,
        ))

    @property
    def notes(self):
        return self.note_set.order_by('-created')

    def set_complete(self, user):
        self.complete = timezone.now()
        self.complete_user = user

    @property
    def time_records(self):
        return self.timerecord_set.order_by('-created')

    @property
    def is_overdue(self):
        return self.due < date.today()

reversion.register(Ticket)


class Note(TimeStampedModel):

    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def deleted(self):
        """No actual delete (yet), so just return 'False'."""
        return False

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.ticket.pk])

    def get_summary_description(self):
        return filter(None, (
            self.title,
            self.description,
        ))

    def modified_today(self):
        return self.created.date() == date.today()

reversion.register(Note)
