# coding: utf-8

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Div, Fieldset, Submit, Field, HTML

from captcha.fields import ReCaptchaField
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(label='email')
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password', max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='again', max_length=76, widget=forms.PasswordInput)
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            HTML('\
              <div class="row">\
                <div class="columns large-6">\
                  <label for="id_username" class="requiredField">\
                    username\
                  </label>\
                  <input id="id_username" maxlength="30" name="username" type="text" required pattern="username"/>\
                  <small class="error">3-30 characters, a-z A-Z 0-9 _ .</small>\
                </div>\
                <div class="columns large-6">\
                  <label for="id_email" class="requiredField">\
                    email\
                  </label>\
                  <input id="id_email" name="email" type="email" required/>\
                  <small class="error">A valid email address is required.</small>\
                </div>\
              </div>\
                \
              <div class="row">\
                <div class="columns large-6">\
                  <label for="id_password" class="requiredField">\
                    password\
                  </label>\
                  <input id="id_password" maxlength="76" name="password" type="password" required/>\
                </div>\
                <div class="columns large-6">\
                  <label for="id_password_confirm" class="requiredField">\
                    again\
                  </label>\
                  <input id="id_password_confirm" maxlength="76" name="password_confirm" type="password" required pattern="pass_confirm"/>\
                  <small class="error">password mismatch</small>\
                </div>\
              </div>\
                \
              <div class="row">\
                <div class="columns large-2">\
            '),
            Field('captcha'),
            HTML('\
                </div>\
                <div class="columns large-4">\
                  <input type="submit" name="submit" value="Register" class="submit button" id="register"/>\
                  <a href="/" class="button secondary">Cancel</a>\
                </div>\
              </div>\
                \
            </form>\
            ')
        )
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Passwords mismatch'
            self._errors['password'] = self.error_class([''])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password' in cleaned_data:
                del cleaned_data['password']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            msg = u'Username already taken'
            self._errors['username'] = self.error_class([msg])

        return cleaned_data


class ProfileForm(forms.Form):
    about = forms.CharField(label='about yourself', required=False, widget=forms.Textarea())
    email = forms.EmailField(label='email')

    # display a select with languages ordered by most used first
    from resrc.language.models import Language
    languages = forms.ModelMultipleChoiceField(label='languages', widget=forms.SelectMultiple(), queryset=Language.objects.all())
    show_email = forms.BooleanField(label='show email', required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Public profile',
                Field('about'),
                Field('email'),
                Field('languages'),
                Field('show_email'),
            ),
            Div(
                Submit('submit', 'Edit my profile', css_class='small'),
                css_class='button-group'
            )
        )
        super(ProfileForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(forms.Form):
    password_new = forms.CharField(label='New password ', max_length=76, widget=forms.PasswordInput)
    password_old = forms.CharField(label='Current password ', max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='New password, again ', max_length=76, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.user = user

        self.helper.layout = Layout(
            Fieldset(
                u'Password',
                Field('password_old'),
                Field('password_new'),
                Field('password_confirm'),
            ),
            Div(
                Submit('submit', 'Change password', css_class='small'),
                css_class='button-group'
            )
        )
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        password_old = cleaned_data.get('password_old')
        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        if password_old:
            user_exist = authenticate(username=self.user.username, password=password_old)
            if not user_exist and password_old != "":
                self._errors['password_old'] = self.error_class([u'Old password incorrect'])
                if 'password_old' in cleaned_data:
                    del cleaned_data['password_old']

        if not password_confirm == password_new:
            msg = u'Password mismatch'
            self._errors['password_new'] = self.error_class([msg])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password_new' in cleaned_data:
                del cleaned_data['password_new']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        return cleaned_data
