from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Industry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Industry)


class Contact(TimeStampedModel):
    """ Contact """
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

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    def get_absolute_url(self):
        return reverse('crm.contact.detail', args=[self.slug])

    def get_summary_description(self):
        return (
            self.name,
            self.address,
        )

reversion.register(Contact)


class UserContact(TimeStampedModel):
    """
    A user is linked to a single contact.
    More than one user can link to the same contact, but a user cannot
    link to more than one contact.

    e.g.
    Andy - ConnexionSW
    Fred - ConnexionSW
    Kate - British Sugar
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return unicode('{} - {}'.format(self.user.username, self.contact.name))


class Priority(models.Model):
    """Level 0 will exclude the ticket from normal reminder lists"""
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()

    class Meta:
        ordering = ('-level', 'name',)
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Priority)


class Ticket(TimeStampedModel):
    """ Contact """
    contact = models.ForeignKey(Contact)
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

    class Meta:
        ordering = ('-complete', 'due', '-priority__level', 'created',)
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.pk])

    def get_summary_description(self):
        return (
            self.title,
            self.description,
        )

    def set_complete(self, user):
        self.complete = datetime.now()
        self.complete_user = user

reversion.register(Ticket)


class Note(TimeStampedModel):
    """ Contact """
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __unicode__(self):
        return unicode('{}'.format(self.title))

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.ticket.pk])

    def modified_today(self):
        return self.created.date() == datetime.today().date()

reversion.register(Note)
