from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from forum.models import ForumPost, ForumCommentPost
from cycle_calendar.models import UserShareCalendar


@login_required
def dashboard(request):
    post_forum = ForumPost.objects.filter(author=request.user, published_date__lte=timezone.now()).order_by(
        'published_date').first()
    comment_forum = ForumCommentPost.objects.filter(author=request.user, approved_comment=True).order_by(
        'created_date').first()

    user_share_list = UserShareCalendar.objects.filter(following=request.user).values()
    user_follow_auth = list(user_share_list)

    user_follower_list = UserShareCalendar.objects.filter(user=request.user).values()
    user_share_auth = list(user_follower_list)

    return render(request, 'users/dashboard.html', {'section': 'dashboard',
                                                    'post_forum': post_forum,
                                                    'comment_forum': comment_forum,
                                                    'user_follow_auth': user_follow_auth,
                                                    'user_share_auth': user_share_auth
                                                    })


def register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'users/register_done.html',
                          {'new_user': new_user},
                          )

    else:
        user_form = UserRegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane.')

            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form_login': form})


@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'users/edit_done.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'users/edit.html', {'user_form': user_form,
                                               'profile_form': profile_form,
                                               })
