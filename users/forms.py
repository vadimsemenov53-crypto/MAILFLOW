from mailflow.forms import StyleFromMixin
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm


class UserRegisterForm(StyleFromMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFromMixin, AuthenticationForm):
    pass


class UserProfileForm(StyleFromMixin, ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'country', 'phone')
