from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_filter(path):
    if path:
        # Используем MEDIA_URL для корректного префикса
        return f"{settings.MEDIA_URL}{path}"
    return '#'