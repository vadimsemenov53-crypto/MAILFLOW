from django.urls import path
from mailflow.apps import MailflowConfig
from mailflow.views import (
    NewsLetterListView,
    NewsLetterCreateView,
    NewsLetterDetailView,
    NewsLetterUpdateView,
    NewsLetterDeleteView,
    NewsLetterRecipientListView,
    NewsLetterRecipientCreateView,
    NewsLetterRecipientDetailView,
    NewsLetterRecipientUpdateView,
    NewsLetterRecipientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
    NewsLetterStartView,
    AttemptedMailingListView,
    AttemptedMailingDetailView,
    AttemptedMailingDeleteView
)

app_name = MailflowConfig.name

urlpatterns = [
    path('mailings/', NewsLetterListView.as_view(), name='mailings_list'),
    path('mailings/create/', NewsLetterCreateView.as_view(), name='mailings_create'),
    path('mailings/<int:pk>/', NewsLetterDetailView.as_view(), name='mailings_detail'),
    path('mailings/<int:pk>/update/', NewsLetterUpdateView.as_view(), name='mailings_update'),
    path('mailings/<int:pk>/delete/', NewsLetterDeleteView.as_view(), name='mailings_delete'),
    path("mailings/<int:pk>/start/", NewsLetterStartView.as_view(), name="mailings_start", ),

    path('recipients/', NewsLetterRecipientListView.as_view(), name='recipients_list'),
    path('recipients/create/', NewsLetterRecipientCreateView.as_view(), name='recipients_create'),
    path('recipients/<int:pk>/', NewsLetterRecipientDetailView.as_view(), name='recipients_detail'),
    path('recipients/<int:pk>/update/', NewsLetterRecipientUpdateView.as_view(), name='recipients_update'),
    path('recipients/<int:pk>/delete/', NewsLetterRecipientDeleteView.as_view(), name='recipients_delete'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('attempts/', AttemptedMailingListView.as_view(), name='attempts_list'),
    path('attempts/<int:pk>/', AttemptedMailingDetailView.as_view(), name='attempts_detail'),
    path('attempts/<int:pk>/delete/', AttemptedMailingDeleteView.as_view(), name='attempts_delete'),
]
