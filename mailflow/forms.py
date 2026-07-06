from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from mailflow.models import NewsLetter, NewsLetterRecipient, Message

class StyleFromMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-switch'
            else:
                field.widget.attrs['class'] = 'form-control'


class NewsLetterForm(StyleFromMixin, forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ("name", "time_start", "time_stop", "message", "recipients",)

    def clean_time_start(self):
        now = timezone.now()
        time_start = self.cleaned_data.get('time_start')

        if time_start and time_start < now:
            raise ValidationError('Время старта не может быть в прошлом!')

        return time_start

    def clean_time_stop(self):
        now = timezone.now()
        time_stop = self.cleaned_data.get('time_stop')

        if time_stop and time_stop < now:
            raise  ValidationError('Время конца отправки не может быть в прошлом!')

        return time_stop

    def clean(self):
        cleaned_data = super().clean()
        time_start = cleaned_data.get("time_start")
        time_stop = cleaned_data.get("time_stop")

        if time_start and time_stop:
            if time_start >= time_stop:
                raise ValidationError('Дата начала должна быть раньше даты окончания рассылки!')

        return cleaned_data


class NewsLetterRecipientForm(StyleFromMixin, forms.ModelForm):
    class Meta:
        model = NewsLetterRecipient
        fields = ("email", "first_name", "last_name", "surname", "comment",)


class MessageForm(StyleFromMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body",)

