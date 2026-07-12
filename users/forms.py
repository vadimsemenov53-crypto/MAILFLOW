from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm
from django.forms import ModelForm

from mailflow.forms import StyleFromMixin

from .models import User


class UserRegisterForm(StyleFromMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserLoginForm(StyleFromMixin, AuthenticationForm):
    pass


class UserProfileForm(StyleFromMixin, ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "country", "phone")


class UserPasswordResetConfirmForm(StyleFromMixin, SetPasswordForm):
    pass
