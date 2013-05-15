# -*- encoding: utf-8 -*-
from django.test import TestCase

from .tasks import update_top_comments

class TopCommentTest(TestCase):
    def setUp(self):
        pass

    def test_celery_task(self):
        """
        Tests celery task to get top comments
        """
        result = update_top_comments.delay()
        # wait for 5 seconds to see if taks is over
        result.wait(timeout=5)
        self.assertTrue(result.successful())
        self.assertEqual(result.status, 'SUCCESS')
        self.assertTrue(result.ready())


