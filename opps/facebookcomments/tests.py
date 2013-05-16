# -*- encoding: utf-8 -*-
from django.test import TestCase

from .tasks import update_weekly_posts, update_all_published_posts

class TopCommentTest(TestCase):
    def setUp(self):
        pass

    def test_celery_update_weekly_posts(self):
        """
        Tests celery task to get top comments
        """
        result = update_weekly_posts.delay()
        # wait for 5 seconds to see if taks is over
        result.wait(timeout=5)
        self.assertTrue(result.successful())
        self.assertEqual(result.status, 'SUCCESS')
        self.assertTrue(result.ready())


    def test_celery_update_all_published_posts(self):
        result = update_all_published_posts.delay()
        # wait for 5 seconds to see if taks is over
        result.wait(timeout=5)
        self.assertTrue(result.successful())
        self.assertEqual(result.status, 'SUCCESS')
        self.assertTrue(result.ready())


