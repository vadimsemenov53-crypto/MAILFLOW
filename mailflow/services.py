from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from mailflow.models import NewsLetter
from config.settings import EMAIL_HOST_USER

def send_newsletter(newsletters):
    """ Функция для реализации отправки рассылки по указанным адресам. """
    newsletters.update_status()

    if newsletters.status != NewsLetter.ST_LAUNCHED:
        raise ValidationError('В данное время рассылка не может быть запущена.')

    recipients = newsletters.recipients.all()

    for recipient in recipients:
        send_mail(
            subject=newsletters.message.subject,
            message=newsletters.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[recipient]
        )



