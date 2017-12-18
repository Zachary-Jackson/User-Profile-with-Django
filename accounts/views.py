from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


def sign_in(request):
    '''This view allows the user to sign into the website.'''
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    '''This allows a user to create a new account'''
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    '''This allows a user to sign out of an account.'''
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_view(request):
    '''This takes a logged in user to the user's profile page.'''
    return render(request, 'accounts/profile_view.html')


@login_required
def profile_edit(request):
    '''This takes a logged in user to the user's profile edit page.'''
    form = forms.ProfileForm()
    if request.method == 'POST':
        form = forms.ProfileForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user = User
            form.save()
            messages.success(
                request,
                "You have edited Your profile!"
            )
            return render(request, 'accounts/profile_view.html')
    return render(request, 'accounts/profile_edit.html', {'form': form})
