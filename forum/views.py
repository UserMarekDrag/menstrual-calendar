from django.shortcuts import render
from .models import ForumPost


def forum_post_list(request):
    forum_posts = ForumPost.objects.order_by('category')
    return render(request, 'forum/forum_list.html', {'forum_posts': forum_posts})
