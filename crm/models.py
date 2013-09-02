from django.contrib.auth.models import User
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Contact(TimeStampedModel):
    """ Contact """
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    slug = models.SlugField()
    url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    mail = models.EmailField(blank=True)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Contact)
