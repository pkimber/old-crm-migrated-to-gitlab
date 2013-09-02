from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Contact(TimeStampedModel):
    """ Contact """
    name = models.CharField(max_length=100)
    address = models.TextField()
    url = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=100)
    mail = models.EmailField()

    class Meta:
        ordering = ['section', 'order', 'modified']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __unicode__(self):
        return unicode('{}'.format(self.name))

reversion.register(Simple)
