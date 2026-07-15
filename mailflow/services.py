from config.settings import CACHE_ENABLE
from mailflow.models import NewsLetter, NewsLetterRecipient, AttemptedMailing, Message
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from mailflow.models import NewsLetter, AttemptedMailing
from config.settings import EMAIL_HOST_USER
from django.utils import timezone


def send_newsletter(newsletter):
    """ Функция для реализации отправки рассылки по указанным адресам. """
    newsletter.update_status()

    if newsletter.status == NewsLetter.ST_CREATED:
        raise ValidationError('В данное время рассылка не может быть запущена.')

    if newsletter.status == NewsLetter.ST_COMPLETED:
        raise ValidationError('Рассылка уже завершена!')

    recipients = newsletter.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=newsletter.message.subject,
                message=newsletter.message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[recipient.email]
            )

            AttemptedMailing.objects.create(
                status=AttemptedMailing.ST_SUCCESS,
                response_server=f"Успешно по адресу: {recipient.email}",
                newsletter=newsletter,
                recipient=recipient
            )

        except Exception as e:
            AttemptedMailing.objects.create(
                status=AttemptedMailing.ST_FAILED,
                response_server=f"Ошибка по адресу: {recipient.email} -> ({e})",
                newsletter=newsletter,
                recipient=recipient
            )


class MailFlowService:
    """ Класс для работы сервисной логики и кеширования данных приложения MailFlow. """
    @staticmethod
    def update_newsletters_status(user):
        """ Метод для обновления статусов рассылок на актуальные """
        newsletters = NewsLetter.objects.filter(creator=user)

        changed = False

        for newsletter in newsletters:
            old_status = newsletter.status

            newsletter.update_status()

            if old_status != newsletter.status:
                changed = True

        if changed:
            cache.delete(f"total_mailings_{user.id}")
            cache.delete(f"active_mailings_{user.pk}")



    @staticmethod
    def get_newsletter_count_cache(user):
        """ Метод получения количества рассылок из кеша для переданного Юзера, если кеш - None, то получается данные из БД. """
        if not CACHE_ENABLE:
            return NewsLetter.objects.filter(creator=user).count()

        key = f'total_mailings_{user.id}'
        newsletters = cache.get(key)

        if newsletters is not None:
            return newsletters

        newsletters = NewsLetter.objects.filter(creator=user).count()
        cache.set(key, newsletters, 60 * 2)

        return newsletters

    @staticmethod
    def get_active_newsletters_count_cache(user):
        """ Метод получения количества активных из кеша для переданного Юзера, если кеш - None, то получается данные из БД. """
        now = timezone.now()

        if not CACHE_ENABLE:
            return NewsLetter.objects.filter(
                time_start__lte=now,
                time_stop__gte=now,
                status=NewsLetter.ST_LAUNCHED,
                creator=user
            ).count()

        key = f'active_mailings_{user.id}'
        active_newsletters = cache.get(key)

        if active_newsletters is not None:
            return active_newsletters

        active_newsletters = NewsLetter.objects.filter(
            time_start__lte=now,
            time_stop__gte=now,
            status=NewsLetter.ST_LAUNCHED,
            creator=user
        ).count()

        cache.set(key, active_newsletters, 60 * 2)

        return active_newsletters

    @staticmethod
    def get_recipients_count_cache(user):
        """ Метод получения количества клиентов из кеша для переданного Юзера, если кеш - None, то получается данные из БД. """
        if not CACHE_ENABLE:
            return NewsLetterRecipient.objects.filter(creator=user).count()

        key = f'total_recipients_{user.id}'
        count_recipient = cache.get(key)

        if count_recipient is not None:
            return count_recipient

        count_recipient = NewsLetterRecipient.objects.filter(creator=user).count()

        cache.set(key, count_recipient, 60 * 2)

        return count_recipient
