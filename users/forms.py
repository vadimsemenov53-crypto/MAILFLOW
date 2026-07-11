from mailflow.forms import StyleFromMixin
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(StyleFromMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(StyleFromMixin, AuthenticationForm):
    pass