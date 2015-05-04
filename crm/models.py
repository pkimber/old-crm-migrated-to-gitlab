# -*- encoding: utf-8 -*-
from datetime import date
from dateutil.rrule import (
    MONTHLY,
    rrule,
)

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

import reversion

from base.model_utils import (
    copy_model_instance,
    TimeStampedModel,
)


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

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def deleted(self):
        """No actual delete (yet), so just return 'False'."""
        return False

    def get_absolute_url(self):
        return reverse('crm.contact.detail', args=[self.slug])

    def get_summary_description(self):
        return filter(None, (
            self.name,
            self.address,
        ))

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

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.contact.name)


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

    def set_complete(self, user):
        self.complete = timezone.now()
        self.complete_user = user

    @property
    def is_overdue(self):
        return self.due < date.today()

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


class TaskManager(models.Manager):

    def create_task_recurrence(self, task, user):
        if task.recurrence:
            obj = copy_model_instance(task)
            obj.user = user
            obj.complete = None
            obj.complete_user = None
            obj.recurrence_increment()
            obj.save()


class Task(TimeStampedModel):
    """Task."""

    END_OF_MONTH = 1

    RECURRENCE_CHOICES = (
        (END_OF_MONTH, 'End of Month'),
    )

    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    recurrence = models.IntegerField(choices=RECURRENCE_CHOICES, blank=True, null=True)
    # copy of fields from the ticket model
    due = models.DateTimeField(blank=True, null=True)
    complete = models.DateTimeField(blank=True, null=True)
    complete_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    user_assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    objects = TaskManager()

    class Meta:
        ordering = ('created',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def get_absolute_url(self):
        return reverse('crm.ticket.detail', args=[self.ticket.pk])

    def can_edit(self):
        return self.modified_today and not self.complete

    def recurrence_init(self):
        if self.recurrence == self.END_OF_MONTH:
            today = timezone.now()
            rule = rrule(MONTHLY, bymonthday=(-1,), dtstart=today)
            self.due = rule.after(today)

    def recurrence_increment(self):
        if self.recurrence == self.END_OF_MONTH:
            rule = rrule(MONTHLY, bymonthday=(-1,), dtstart=self.due)
            self.due = rule.after(self.due)

    def modified_today(self):
        return self.created.date() == date.today()

    def set_complete(self, user):
        self.complete = timezone.now()
        self.complete_user = user

reversion.register(Task)
