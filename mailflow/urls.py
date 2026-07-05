from django.urls import path
from mailflow.apps import MailflowConfig
from mailflow.views import (
    NewsLetterListView,
    NewsLetterCreateView,
    NewsLetterDetailView,
    NewsLetterUpdateView,
    NewsLetterDeleteView,
    NewsLetterRecipientListView,
    NewsLetterRecipientCreateView
)

app_name = MailflowConfig.name

urlpatterns = [
    path('mailings/', NewsLetterListView.as_view(), name='mailings_list'),
    path('mailings/create/', NewsLetterCreateView.as_view(), name='mailings_create'),
    path('mailings/<int:pk>/', NewsLetterDetailView.as_view(), name='mailings_detail'),
    path('mailings/<int:pk>/update', NewsLetterUpdateView.as_view(), name='mailings_update'),
    path('mailings/<int:pk>/delete', NewsLetterDeleteView.as_view(), name='mailings_delete'),

    path('recipients/', NewsLetterRecipientListView.as_view(), name='recipients_list'),
    path('recipients/create/', NewsLetterRecipientCreateView.as_view(), name='recipients_create')
]
