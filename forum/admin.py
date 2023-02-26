from django.contrib import admin
from .models import ForumPost, ForumCommentPost

admin.site.register(ForumPost)
admin.site.register(ForumCommentPost)
