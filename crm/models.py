# -*- encoding: utf-8 -*-
from datetime import date

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

#from mptt.models import (
#    MPTTModel,
#    TreeForeignKey,
#)
import reversion

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


class Contact(TimeStampedModel):

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    mail = models.EmailField(blank=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    hourly_rate = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=2
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def deleted(self):
        """No actual delete (yet), so just return 'False'."""
        return False

    def get_absolute_url(self):
        return reverse('contact.detail', args=[self.slug])

    def get_summary_description(self):
        return filter(None, (
            self.name,
            self.address,
        ))

reversion.register(Contact)


class CrmContact(TimeStampedModel):

    contact = models.OneToOneField(settings.CONTACT_MODEL)
    industry = models.ForeignKey(Industry, blank=True, null=True)

    class Meta:
        verbose_name = 'CRM Contact'
        verbose_name_plural = 'CRM Contacts'

    def __str__(self):
        return '{}'.format(self.contact.name)

reversion.register(CrmContact)


# class UserContact(TimeStampedModel):
#     """
#     A user is linked to a single contact.
#     More than one user can link to the same contact, but a user cannot
#     link to more than one contact.
#
#     e.g.
#     Andy - ConnexionSW
#     Fred - ConnexionSW
#     Kate - British Sugar
#
#     25/01/2016 Is not used on the KB CRM system, so we will remove it.
#
#     """
#
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user')
#     contact = models.ForeignKey(Contact)
#     # PJK1
#     # new_contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='usercontact_contact')
#
#     # contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='contact')
#     # crm_contact = models.ForeignKey(Contact)
#     # crm_contact = models.ForeignKey(Contact) #, related_name='crm_contact_user_contact')
#     # PJK2
#     # contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='user_contact_contact')
#
#     def __str__(self):
#         return '{} - {}'.format(self.user.username, self.contact.name)


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

    def current(self):
        return self.model.objects.filter(complete__isnull=True)

    def planner(self):
        return self.model.objects.filter(
            complete__isnull=True
        ).exclude(
            priority__level=0
        )


# mptt
# class Ticket(MPTTModel):
class Ticket(TimeStampedModel):

    # mptt
    # parent = TreeForeignKey(
    #     'self', null=True, blank=True, related_name='children', db_index=True
    # )
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)

    # PJK3
    # contact = models.ForeignKey(Contact)
    # PJK2
    # new_contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='ticket_contact')
    # PJK3
    # new_contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='ticket_contact')
    # PJK4
    contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='ticket_contact')

    # contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True)
    # contact = models.ForeignKey(settings.CONTACT_MODEL)
    # crm_contact = models.ForeignKey(Contact)
    # crm_contact = models.ForeignKey(Contact) #, related_name='crm_contact_ticket')
    # PJK2
    # contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='ticket_contact')
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
    objects = TicketManager()

    class Meta:
        ordering = ('-complete', 'due', '-priority__level', 'created',)
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def deleted(self):
        """No actual delete (yet), so just return 'False'."""
        return False

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
