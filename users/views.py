from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html', {'section': 'dashboard'})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("user/")

        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()

    return render(request, 'users/register.html', {"register_form": form})


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

    return render(request, 'user/login.html', {'form_login': form})
