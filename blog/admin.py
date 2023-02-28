from django.contrib import admin
from .models import Post, CommentPost, Category

admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(Category)
