# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import TopComment

class TopCommentAdmin(admin.ModelAdmin):
    model = TopComment

    raw_id_fields = ('post', )

    list_display = ('post', 'comment_text', 'comment_count', 'date_added')

admin.site.register(TopComment, TopCommentAdmin)
