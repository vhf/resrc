# -*- coding: utf-8 -*-:
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.core.context_processors import csrf

from resrc.utils.tokens import generate_token
from resrc.utils import render_template

from resrc.userprofile.models import Profile
from resrc.userprofile.forms import LoginForm, ProfileForm, RegisterForm, ChangePasswordForm


def user_list(request):
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


def login_register_view(request, register=False):
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    login_error = False
    if request.method == 'POST' and not register:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['get_token'] = generate_token()
                if not 'remember' in request.POST:
                    request.session.set_expiry(0)
                if 'next' in request.POST:
                    return redirect(request.POST['next'] or '/')
                else:
                    return redirect('/')
            else:
                login_error = 'Bad user/password'
        else:
            login_error = 'Form invalid'

    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST' and register:
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])
            profile = Profile(user=user)
            profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render_template('user/register_success.html')

    csrf_tk['register_form'] = register_form
    csrf_tk['login_error'] = login_error
    csrf_tk['login_form']  = login_form
    csrf_tk['register'] = register
    if 'next' in request.GET:
        csrf_tk['next']  = request.GET.get('next')
    return render_template('user/login_register.html', csrf_tk)


@login_required
def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect('/')


@login_required
def settings_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
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
                return redirect(reverse('user-settings'))

            messages.success(
                request, 'Update successful.')
            return redirect(reverse('user-settings'))
        else:
            return render_template('user/settings_profile.html', {
                'usr': request.user,
                'form': form,
            })
    else:
        print "here"
        form = ProfileForm(initial={
            'about': profile.about,
            'email': request.user.email,
            'show_email': profile.show_email
            }
        )
        return render_template('user/settings_profile.html', {
            'usr': request.user,
            'form': form
        })


@login_required
def settings_account(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request.user)
        if form.is_valid():
            try:
                request.user.set_password(form.data['password_new'])
                request.user.save()
                messages.success(
                    request, 'Password updated.')
                return redirect(reverse('user-settings'))
            except:
                messages.error(request, 'Error while updating your password.')
                return redirect(reverse('user-settings'))
        else:
            return render_template('user/settings_account.html', {
                'usr': request.user,
                'form': form,
            })
    else:
        form = ChangePasswordForm(request.user)
        return render_template('user/settings_account.html', {
            'usr': request.user,
            'form': form,
        })
