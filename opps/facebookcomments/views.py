# -*- encoding: utf-8 -*-
from urllib import urlencode

from django.http import HttpResponse
from django.conf import settings

from opps.articles.models import Post
from facepy import GraphAPI


def test(request):
    posts = Post.objects.all_published().filter(site=settings.SITE_ID)
    # creates a batch facebook request for posts
    token = ('CAACEdEose0cBANjfCgHAkdb8VEUEvj70rLVY72FOyN5e6Pp0MGWA2oZAwhPDUZA'
             '6bs64Sor2GrEvg72HLZCZC9IgucKH68buOZAEnSQAh6HbcOjeTsRVvlRr3f3A2wH'
             'G58HD51kZAN0ata3rXXCbex1hYZCw62GnUyMZB1xC9enDhQZDZD')

    f = GraphAPI(token)
    requests = []
    count = 0
    for post in posts.iterator():
        query = urlencode({'query': "SELECT comment_count FROM link_stat "
                           "WHERE url='{}'".format(
                               post.get_http_absolute_url()
                           )})
        data = {
            'method': 'POST',
            'relative_url': 'method/fql.query?' + query,
        }
        requests.append(data)
        count += 1
        if count == 50:
            # undefined name process_requests
            # process_requests(requests)
            pass
    request = f.batch(requests)
    for result in request:
        print result

    return HttpResponse(requests)
