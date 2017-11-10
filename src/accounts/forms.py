from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from authtools import forms as authtoolsforms
from django.contrib.auth import forms as authforms
from django.core.urlresolvers import reverse


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False, label="记住我")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('username', placeholder="输入用户名", autofocus=""),
            Field('password', placeholder="输入密码"),
            HTML('<a href="{}">忘记密码?</a>'.format(
                reverse("accounts:password-reset"))),
            Field('remember_me'),
            Submit('sign_in', '登录',
                   css_class="btn btn-lg btn-primary btn-block"),
            )


class SignupForm(authtoolsforms.UserCreationForm):
    error_messages = {
        'password_mismatch': "两个密码字段不一致。",
        'duplicate_username': "该电子邮箱已被注册。",
    }
    password2 = forms.CharField(label="密码确认",
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["email"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('email', placeholder="输入电子邮箱", autofocus=""),
            Field('name', placeholder="输入您的姓名"),
            Field('password1', placeholder="密码"),
            Field('password2', placeholder="在此输入密码"),
            Submit('sign_up', '注册', css_class="btn-warning"),
            )


class PasswordChangeForm(authforms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('old_password', placeholder="输入旧密码",
                  autofocus=""),
            Field('new_password1', placeholder="输入新密码"),
            Field('new_password2', placeholder="再次输入新密码"),
            Submit('pass_change', '密码修改', css_class="btn-warning"),
            )


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('email', placeholder="输入电子邮箱",
                  autofocus=""),
            Submit('pass_reset', '密码重置', css_class="btn-warning"),
            )


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('new_password1', placeholder="输入新密码",
                  autofocus=""),
            Field('new_password2', placeholder="再次输入新密码"),
            Submit('pass_change', '修改密码', css_class="btn-warning"),
            )
