from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Industry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Industry)


class Contact(TimeStampedModel):
    """ Contact """
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    slug = models.SlugField()
    url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    mail = models.EmailField(blank=True)
    industry = models.ForeignKey(Industry, blank=True, null=True)
    hourly_rate = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=2
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

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
    user = models.ForeignKey(User, unique=True)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return unicode('{} - {}'.format(self.user.username, self.contact.name))


class Priority(models.Model):
    """Level 0 will exclude the ticket from normal reminder lists"""
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()

    class Meta:
        ordering = ['-level', 'name']
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Priority)


class Ticket(TimeStampedModel):
    """ Contact """
    contact = models.ForeignKey(Contact)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    priority = models.ForeignKey(Priority)
    due = models.DateField(blank=True, null=True)
    complete = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.pk])

reversion.register(Ticket)


class Note(TimeStampedModel):
    """ Contact """
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.ticket.pk])

    def modified_today(self):
        return self.created.date() == datetime.today().date()

reversion.register(Note)
