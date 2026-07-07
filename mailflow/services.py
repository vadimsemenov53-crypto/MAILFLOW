from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from mailflow.models import NewsLetter
from config.settings import EMAIL_HOST_USER

def send_newsletter(newsletter):
    """ Функция для реализации отправки рассылки по указанным адресам. """
    newsletter.update_status()

    if newsletter.status != NewsLetter.ST_LAUNCHED:
        raise ValidationError('В данное время рассылка не может быть запущена.')

    recipients = newsletter.recipients.all()

    for recipient in recipients:
        send_mail(
            subject=newsletter.message.subject,
            message=newsletter.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[recipient.email]
        )



