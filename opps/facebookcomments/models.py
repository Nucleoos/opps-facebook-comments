# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.containers.models import Container


class TopComment(Publishable):
    container = models.OneToOneField(Container)
    profile_name = models.CharField(_(u'Profile Name'),
                                    max_length=255, blank=True)
    comment_text = models.TextField(_(u'Comment'), blank=True)
    comment_count = models.IntegerField(_(u'Comment count'), default=0)
    date_added = models.DateTimeField(_(u'Date added'))

    def __unicode__(self):
        return u"{} - {}".format(self.profile_name, self.comment_text)

    class Meta:
        verbose_name = _(u'Top Comment')
        verbose_name_plural = _(u'Top Comments')
        ordering = ('comment_count', '-id')
