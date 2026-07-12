from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from users.views import UserCreateView, UserLoginView, email_verification, UserDetailView, UserUpdateView
from users.forms import UserPasswordResetConfirmForm

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(next_page='mailflow:main_page'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailflow:main_page'), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('detail/', UserDetailView.as_view(), name='detail'),
    path('update/', UserUpdateView.as_view(), name='update'),

    path("password-reset/", PasswordResetView.as_view(
        template_name="users/password_reset_form.html",
        email_template_name="users/password_reset_email.html",
        success_url="/users/password-reset/done/",
    ), name="password_reset"),

    path("password-reset/done/", PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html",
    ), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        form_class=UserPasswordResetConfirmForm,
        success_url="/users/password-reset/complete/",
    ), name="password_reset_confirm"),

    path("password-reset/complete/", PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html",
    ), name="password_reset_complete", )

]
