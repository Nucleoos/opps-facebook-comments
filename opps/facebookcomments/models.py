# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable
from opps.articles.models import Post

class TopComment(Publishable):
    post = models.OneToOneField(Post)
    comment_count = models.IntegerField(_(u'Total de comentários'), default=0)

    class Meta:
        verbose_name = _(u'Top Comentário')
        verbose_name_plural = _(u'Top Comentários')
        ordering = ('comment_count',)
