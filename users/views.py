import secrets

from django.views.generic import CreateView
from .models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect

from config.settings import EMAIL_HOST_USER

from django.contrib.auth.views import LoginView
from users.forms import UserLoginForm, UserRegisterForm


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

        send_mail(
            subject='MAILFLOW Подтверждение почты',
            message=f'Привет перейди по ссылке для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()

    send_mail(
        subject='MAILFLOW. \n Добро пожаловать в наш сервис!',
        message='Спасибо за регистрацию! Теперь вам доступны все наши возможности отправки рассылок, писем.',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email]
    )

    return redirect(reverse('users:login'))