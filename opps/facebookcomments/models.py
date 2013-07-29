# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.containers.models import Container


class TopComment(Publishable):
    post = models.OneToOneField(Container)
    profile_name = models.CharField(_(u'Nome do comentarista'),
                                    max_length=255, blank=True)
    comment_text = models.TextField(_(u'Comentário'), blank=True)
    comment_count = models.IntegerField(_(u'Total de comentários'), default=0)
    date_added = models.DateTimeField(_(u'Data/Hora do comentário'))

    def __unicode__(self):
        return u"{} - {}".format(self.profile_name, self.comment_text)

    class Meta:
        verbose_name = _(u'Top Comentário')
        verbose_name_plural = _(u'Top Comentários')
        ordering = ('comment_count', '-id')
