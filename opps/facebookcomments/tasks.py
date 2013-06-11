# -*- coding: utf-8 -*-
import datetime
import logging

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

from .models import TopComment

from opps.articles.models import Post
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from facepy import GraphAPI
from facepy.utils import get_application_access_token


def process_posts(posts):
    """
    Do facebook requests for the posts urls and update the comment count
    """

    APP_ID = getattr(settings, 'FACEBOOK_APP_ID', None)
    API_SECRET = getattr(settings, 'FACEBOOK_API_SECRET', None)

    if not APP_ID and API_SECRET:
        raise ImproperlyConfigured('You must have an FACEBOOK_APP_ID and a '
                                   ' FACEBOOK_API_SECRET in your settings.py')

    token = get_application_access_token(APP_ID, API_SECRET)

    graph = GraphAPI(token)

    # print "Queue:", posts.count()

    for post in posts.iterator():
        # print "Processing:", post.slug
        comment_data = get_top_comment_info(
            graph,
            post.get_http_absolute_url()
        )

        # print "get data", comment_data

        if comment_data.get('profile_name'):
            comment_count = comment_data.get('comment_count')
            comment_text = comment_data.get('comment_text')
            profile_name = comment_data.get('profile_name')
            comment_time = comment_data.get('comment_time')

            # TODO: Use get_or_create
            try:
                top = TopComment.objects.get(post=post)
                top.comment_count = comment_count
                top.comment_text = comment_text
                top.profile_name = profile_name
                top.date_added = comment_time
                top.save()
            except TopComment.DoesNotExist:
                # TODO: save each comment in a separate model
                # retrieve only latest published
                TopComment.objects.create(
                    post=post,
                    comment_count=comment_count,
                    profile_name=profile_name,
                    comment_text=comment_text,
                    date_added=comment_time,
                    user=post.user,
                    site=post.site,
                    published=True
                )


@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))
def update_all_published_posts():
    """
    updates the published posts comment count
    """
    posts = Post.objects.all_published().filter(site=settings.SITE_ID)
    process_posts(posts)


@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))
def update_weekly_posts():
    """
    updates the weekly post comment count
    """
    today = timezone.now()
    days_ago = today - timezone.timedelta(days=7)

    posts = Post.objects.all_published().filter(site=settings.SITE_ID)
    posts = posts.filter(date_available__range=(days_ago, today))
    process_posts(posts)


def get_top_comment_info(graph, url):
    """
    Returns facebook comment count, profile pic and comment
    for a given url
    TODO: Use facebook's fql multiquery to get the results
    """
    query1 = (
        "SELECT commentsbox_count FROM "
        "link_stat WHERE url='{}'"
    ).format(url)

    query2 = (
        "SELECT time, fromid, text FROM comment WHERE object_id IN "
        "(SELECT comments_fbid FROM link_stat WHERE url = '{}') ORDER BY "
        "likes DESC LIMIT 1"
    ).format(url)

    comment_count = 0
    comment_text = ''
    profile_name = ''
    profile_id = ''
    comment_time = 0

    # get comment count for url
    try:
        request = graph.fql(query1)
    except Exception as e:
        logging.warning(u'Facebook graph exception on comment count '
                        u'query: %s' % e)
        return {}

    if 'data' in request:
        try:
            comment_count = request['data'][0]['commentsbox_count']
        except IndexError:
            pass

    # get top like comment
    try:
        request = graph.fql(query2)
    except Exception as e:
        logging.warning(u'Facebook graph exception on top like comment: %s' %
                        e)
        return {}

    if 'data' in request:
        try:
            data = request['data'][0]
            comment_text = data['text']
            profile_id = str(data['fromid'])
            comment_time = datetime.datetime.fromtimestamp(data['time'])
        except IndexError:
            pass

    # get top comment user info
    if profile_id.isdigit():
        try:
            user_info = graph.get(profile_id)
        except Exception as e:
            logging.warning(u'Facebook graph exception on get user info: %s'
                            % e)
            return {}
        profile_name = user_info['name']

    comment_data = {
        'comment_text': comment_text,
        'comment_count': comment_count,
        'comment_time': comment_time,
        'profile_name': profile_name,
    }

    return comment_data
