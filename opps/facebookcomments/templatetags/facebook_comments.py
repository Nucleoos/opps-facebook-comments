# -*- encoding: utf-8 -*-
from django import template

from opps.facebookcomments.models import TopComment

register = template.Library()


@register.simple_tag
def get_top_comments(quantity=10,
                     template_name='facebookcomments/top_comments.html'):

    top_comments = TopComment.objects.filter(published=True)[:quantity]
    t = template.loader.get_template(template_name)
    return t.render(template.Context({'comments': top_comments}))
