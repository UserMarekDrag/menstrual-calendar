from django.contrib import admin
from .models import Post, CommentPost

admin.site.register(Post)
admin.site.register(CommentPost)
