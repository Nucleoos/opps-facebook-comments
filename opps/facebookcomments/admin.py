# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import TopComment

class TopCommentAdmin(admin.ModelAdmin):
    model = TopComment
    list_display = ('post', 'comment_count')

    def has_add_permission(self, request):
        return False
