from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumPost
from django.utils import timezone
from .forms import ForumCommentForm


def forum_post_list(request):
    forum_category = ForumPost.objects.values('category').distinct()
    forum_posts = ForumPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'forum/forum_list.html', {'forum_categories': forum_category,
                                                     'forum_posts': forum_posts,
                                                     })


def forum_post_detail(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)

    if request.method == 'POST':
        comment_form = ForumCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('forum_post_detail', pk=post.pk)
    else:
        comment_form = ForumCommentForm()

    return render(request, 'forum/forum_post.html', {'post': post,
                                                     'comment_form': comment_form,
                                                     })
