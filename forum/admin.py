from django.contrib import admin
from .models import ForumPost, ForumCommentPost, Category

admin.site.register(ForumPost)
admin.site.register(ForumCommentPost)
admin.site.register(Category)
