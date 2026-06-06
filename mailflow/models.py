from django.db import models


# Create your models here.


class NewsLetterRecipient(models.Model):
    """ Модель для получателя рассылки """
    email = models.EmailField(
        max_length=250,
        verbose_name='Email получателя',
        unique=True
    )

    first_name = models.CharField(
        max_length=250,
        verbose_name='Имя',
        help_text='Введите имя получателя'
    )

    last_name = models.CharField(
        max_length=250,
        verbose_name='Фамилия',
        help_text='Введите фамилию получателя'
    )

    surname = models.CharField(
        max_length=250,
        verbose_name='Отчество',
        help_text='Введите отчество получателя'
    )

    comment = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите комментарий о получателе',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name} ( {self.email} )'

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['last_name', ]



class Message(models.Model):
    """ Модель для сообщения """
    subject = models.CharField(
        max_length=250,
        verbose_name='Тема письма',
        help_text='Введите тему письма',
    )

    body = models.TextField(
        verbose_name='Тело письма',
        help_text='Введите полное содержание письма'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['-created_at', ]


class NewsLetter(models.Model):
    """ Модель рассылка """
    ST_COMPLETED = 'completed'
    ST_CREATED = 'created'
    ST_LAUNCHED = 'launched'

    STATUS_LETTER_CHOICES = [
        (ST_COMPLETED, 'Завершена'),
        (ST_CREATED, 'Cоздана'),
        (ST_LAUNCHED, 'Запущена'),
    ]

    time_start = models.DateTimeField(
        verbose_name='дата и время первой отправки'
    )

    time_stop = models.DateTimeField(
        verbose_name='дата и время окончания отправки'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_LETTER_CHOICES,
        default=ST_CREATED,
        verbose_name='Статус'
    )

    message = models.ForeignKey(
        Message,
        verbose_name='Сообщение',
        help_text='Выберите сообщение',
        on_delete=models.SET_NULL,
        related_name='newsletters',
        null=True,
        blank=True
    )

    recipients = models.ManyToManyField(
        NewsLetterRecipient,
        verbose_name='Получатели',
        help_text='Введите получателей',
        related_name='recipients'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.status} - {self.message}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['-time_start', ]


class AttemptedMailing(models.Model):
    """ Модель попытки отправки рассылки """
    ST_SUCCESS = 'success'
    ST_FAILED = 'failed'

    STATUS_MAIL_CHOICES = [
        (ST_SUCCESS, 'Успешно'),
        (ST_FAILED, 'Не успешно'),
    ]

    time_mail = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата и время попытки отправки отправки'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_MAIL_CHOICES,
        default=ST_FAILED,
        verbose_name='Статус'
    )

    response_server = models.TextField(
        verbose_name='Ответ почтового сервиса',
        help_text='Введите ответ от сервиса',
        blank=True,
        null=True
    )

    newsletter = models.ForeignKey(
        NewsLetter,
        verbose_name='Рассылка',
        help_text='Выберите рассылку',
        on_delete=models.SET_NULL,
        related_name='attempts',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.status} - {self.newsletter}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['-time_mail', 'status',]