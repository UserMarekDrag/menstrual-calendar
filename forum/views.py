from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumPost, Category, ForumCommentPost
from django.utils import timezone
from .forms import ForumCommentForm, AddPostForm
from django.contrib.auth.decorators import login_required


def forum_post_list(request):
    categories = Category.objects.all()
    posts = ForumPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'forum/forum_list.html', {'categories': categories,
                                                     'posts': posts,
                                                     })


def forum_post_detail(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    categories = Category.objects.all()
    last_posts = ForumPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[:3]
    amount_comments = ForumCommentPost.objects.filter(post=post, approved_comment=True).count()

    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = ForumCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('forum_post_detail', pk=post.pk)
        else:
            comment_form = ForumCommentForm()
    else:
        comment_form = ForumCommentForm()

    return render(request, 'forum/forum_post.html', {'post': post,
                                                     'comment_form': comment_form,
                                                     'categories': categories,
                                                     'last_posts': last_posts,
                                                     'amount_comments': amount_comments,
                                                     })


def forum_category_detail(request, name):
    category_name = str(name)
    categories = Category.objects.filter(name=category_name).values()
    posts = ForumPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'forum/forum_category_detail.html', {'categories': categories,
                                                                'posts': posts,
                                                                })


@login_required
def new_post(request):

    if request.method == 'POST':
        post_form = AddPostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('done_post')

    else:
        post_form = AddPostForm()

    return render(request, 'forum/new_post.html', {'post_form': post_form})


@login_required
def done_post(request):
    return render(request, 'forum/add_post_done.html', {'section': 'done_post'})
