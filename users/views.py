import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from config.settings import EMAIL_HOST_USER
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm

from .models import User


# Create your views here.
class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm


class UserListView(LoginRequiredMixin, PermissionRequiredMixin,  ListView):
    model = User
    permission_required = "users.view_user"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return User.objects.exclude(
            groups__name="Managers"
        ).exclude(
            is_superuser=True
        )


class UserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_manager:
            raise PermissionDenied

        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            raise PermissionDenied

        if user.is_manager:
            raise PermissionDenied

        user.is_active = False
        user.save()

        return redirect("users:list_users")


class UserUnBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_manager:
            raise PermissionDenied

        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            raise PermissionDenied

        if user.is_manager:
            raise PermissionDenied

        user.is_active = True
        user.save()

        return redirect("users:list_users")


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"

        send_mail(
            subject="MAILFLOW Подтверждение почты",
            message=f"Привет перейди по ссылке для подтверждения почты: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()

    send_mail(
        subject="MAILFLOW. Добро пожаловать в наш сервис!",
        message="Спасибо за регистрацию! Теперь вам доступны все наши возможности отправки рассылок, писем.",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
    )

    return redirect(reverse("users:login"))


@method_decorator(cache_page(60 * 5), name='dispatch')
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"

    def get_object(self):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:detail")
