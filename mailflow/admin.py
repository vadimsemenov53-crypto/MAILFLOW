from django.contrib import admin
from .models import NewsLetterRecipient, Message, NewsLetter, AttemptedMailing

# Register your models here.

@admin.register(NewsLetterRecipient)
class NewsLetterRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('email', 'first_name', 'last_name',)

    @admin.display(description="ФИО")
    def full_name(self, obj):
        return obj.full_name


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subject', 'body',)


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('status', 'time_start', 'time_stop', 'created_at',)
    list_filter = ('status', 'message', 'created_at',)
    search_fields = ('status', 'message__subject', 'message__body',)
    date_hierarchy = 'created_at'


@admin.register(AttemptedMailing)
class AttemptedMailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'time_mail', 'newsletter_status')
    list_filter = ('status', 'time_mail',)
    search_fields = ('status', 'newsletter__message__subject', 'response_server',)

    @admin.display(description='Статус рассылки')
    def newsletter_status(self, obj):
        return obj.newsletter.status if obj.newsletter else '-'
