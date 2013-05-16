# -*- coding: utf-8 -*-
from urllib import urlencode

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from .models import TopComment

from opps.articles.models import Post
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from facepy import GraphAPI
from facepy.utils import get_application_access_token

@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))
def update_top_comments():
    """
    updates the top comments
    """
    if not hasattr(settings, 'FACEBOOK_APP_ID') :
        raise ImproperlyConfigured('You must have an FACEBOOK_APP_ID and a '
                                   ' FACEBOOK_API_SECRET in your settings.py')

    today = timezone.now()
    days_ago = today - timezone.timedelta(days=7)

    posts = Post.objects.all_published().filter(site=settings.SITE_ID)
    posts = posts.filter(date_available__range=(days_ago, today))

    requests = []
    count = 0

    token =  get_application_access_token(settings.FACEBOOK_APP_ID,
                                          settings.FACEBOOK_API_SECRET)

    f = GraphAPI(token)

    for post in posts.iterator():
        # FOR BATCH REQUEST WE NEED A VALID TOKEN OR APP_ID
        # MAX 50 BATCH REQUESTS PER TIME

        query = urlencode({'query': 'SELECT comment_count FROM link_stat '
                           'WHERE url="{}"'.format(
                               post.get_http_absolute_url()
                           )})

        data = {
            'method': 'GET',
            'relative_url': 'method/fql.query?' + query,
        }
        requests.append(data)
        count += 1
        if count == 50:
            request = f.batch(requests)
            for result in request:
                comment_count = 0
                if result:
                    comment_count = result[0]['comment_count']

                if comment_count > 0:
                    try:
                        top = TopComment.objects.get(post=post)
                        top.comment_count = comment_count
                        top.save()
                    except TopComment.DoesNotExist:
                        TopComment.objects.create(post=post,
                                                  comment_count=comment_count,
                                                  user=post.user,
                                                  site=post.site)
            count = 0
            requests = []


def get_comment_count(obj):
    """
    Retorna a quantidade de comentarios da url usando FQL
    """
    graph = GraphAPI()
    comments_count = 0
    query = 'SELECT comment_count FROM link_stat WHERE url = "{}"'.format(
        obj.get_http_absolute_url(),
    )
    request = graph.fql(query, retry=1)
    if 'data' in request:
        comments_count = request['data'][0]['comment_count']
    else:
        comments_count = 0
    return comments_count
