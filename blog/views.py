from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, CommentPost
from .forms import CommentForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    last_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[:6]
    categories = Category.objects.all()
    amount_comments = CommentPost.objects.filter(post=post, approved_comment=True).count()
    posts_alphabetically = Post.objects.order_by('title')[:10]
    user_auth = request.user.is_authenticated
    error_author = ''

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if user_auth:
                comment.author = request.user
            comment.post = post
            if comment.author:
                comment.save()
                return redirect('post_detail', pk=post.pk)
            else:
                error_author = 'Error no Author typed'
                form = CommentForm()

    else:
        form = CommentForm()
    return render(request, 'blog/post.html', {'post': post,
                                              'form': form,
                                              'last_posts': last_posts,
                                              'categories': categories,
                                              'amount_comments': amount_comments,
                                              'posts_alphabetically': posts_alphabetically,
                                              'user_auth': user_auth,
                                              'error_author': error_author,
                                              })


def category_detail(request, name):
    category_name = str(name)
    categories = Category.objects.filter(name=category_name).values()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/category_posts.html', {'categories': categories,
                                                        'posts': posts,
                                                        })


def about(request):
    return render(request, 'blog/about.html', {'section': 'home'})
