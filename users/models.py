from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Введите адрес эл.почты')
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        blank=True, null=True,
        help_text='Загрузите фото для автара'
    )

    phone = PhoneNumberField(
        verbose_name='Телефон',
        blank=True, null=True,
        help_text='Введите номер телефона.'
    )

    country = models.CharField(
        max_length=50,
        verbose_name='Страна',
        blank=True, null=True,
        help_text='Введите страну'
    )

    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
