from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from mailflow.models import NewsLetter, AttemptedMailing
from config.settings import EMAIL_HOST_USER

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




