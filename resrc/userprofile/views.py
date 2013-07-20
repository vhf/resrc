# coding: utf-8

from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.http import Http404

from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.context_processors import csrf
from django.template import RequestContext

from resrc.utils.tokens import generate_token
from resrc.utils import render_template

from .models import Profile
from .forms import LoginForm, ProfileForm, RegisterForm, ChangePasswordForm

from resrc.link.models import Link
from resrc.list.models import List


def user_list(request):
    '''user directory'''
    #profiles = Profile.objects.select_related('User').order_by('user__date_joined')
    users = User.objects.exclude(username='root')
    return render_template('user/list.html', {
        'users': list(users)
    })


def details(request, user_name):
    '''Displays details about a profile'''
    usr = get_object_or_404(User, username=user_name)

    try:
        profile = Profile.objects.get(user=usr)
    except SiteProfileNotAvailable:
        raise Http404

    return render_template('user/profile.html', {
        'usr': usr,
        'profile': profile
    })


def login_view(request):
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['get_token'] = generate_token()
                if not 'remember' in request.POST:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                error = 'Bad user/password'
        else:
            error = 'Form invalid'
    else:
        form = LoginForm()
    csrf_tk['error'] = error
    csrf_tk['form'] = form
    return render_template('user/login.html', csrf_tk)


@login_required
def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])
            profile = Profile(user=user)
            profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render_template('user/register_success.html')
        else:
            return render_template('user/register.html', {'form': form})

    form = RegisterForm()
    return render_template('user/register.html', {
        'form': form
    })


# settings for public profile

@login_required
def settings_profile(request):
    # extra information about the current user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            profile.about = form.data['about']
            request.user.email = form.data['email']
            if 'show_email' in form.data:
                profile.show_email = form.data['show_email']
            else:
                profile.show_email = False

            # Save the profile
            # and redirect the user to the configuration space
            # with message indicate the state of the operation
            try:
                profile.save()
                request.user.save()
            except:
                messages.error(request, 'Error')
                return redirect('/u/edit')

            messages.success(
                request, 'Update successful.')
            return redirect('/u/edit')
        else:
            return render_to_response('user/settings_profile.html', c, RequestContext(request))
    else:
        form = ProfileForm(request.user, initial={
            'about': profile.about,
            'email': request.user.email,
            'show_email': profile.show_email
            }
        )
        c = {
            'form': form
        }
        return render_to_response('user/settings_profile.html', c, RequestContext(request))


@login_required
def settings_account(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            try:
                request.user.set_password(form.data['password_new'])
                request.user.save()
                messages.success(
                    request, 'Password updated.')
                return redirect('/u/edit')
            except:
                messages.error(request, 'Error while updating your password.')
                return redirect('/u/edit')
        else:
            return render_to_response('user/settings_account.html', c, RequestContext(request))
    else:
        form = ChangePasswordForm(request.user)
        c = {
            'form': form,
        }
        return render_to_response('user/settings_account.html', c, RequestContext(request))
