from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models


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
def change_password(request):
    '''This allows the user to change passwords.'''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # This checks to see if the old and new passwords are the same.
            old = form.cleaned_data['old_password']
            new = form.cleaned_data['new_password1']
            if old == new:
                messages.error(request, 'You can not reuse your old password.')
            else:
                form.save()
                messages.success(request, 'You have updated your password.')
                return HttpResponseRedirect(reverse('home'))
    form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html',
                  {'form': form})


@login_required
def profile_view(request):
    '''This takes a logged in user to the user's profile page.'''
    return render(request,
                  'accounts/profile_view.html')


@login_required
def profile_edit(request):
    '''This takes a logged in user to the user's profile edit page.'''
    # This checks to see if the user already has a profile.
    try:
        profile = models.Profile.objects.get(user=request.user.id)
    except ObjectDoesNotExist:
        # This creates a ProfileForm for the user.
        form = forms.ProfileForm(initial={'user': request.user.id})
        if request.method == 'POST':
            form = forms.ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                messages.success(
                    request,
                    "You have created Your profile!"
                )
                return render(request, 'accounts/profile_view.html')
    else:
        # This takes the user's profile and sends it into the form.
        request.user.profile = profile
        form = forms.ProfileForm(instance=profile, initial={
            'email_confirmation': profile.email})
        if request.method == 'POST':
            form = forms.ProfileForm(request.POST, request.FILES,
                                     instance=profile)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "You have edited Your profile!"
                )
                return render(request, 'accounts/profile_view.html')
    return render(request, 'accounts/profile_edit.html', {'form': form})
