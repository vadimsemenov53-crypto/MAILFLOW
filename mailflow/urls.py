from django.urls import path
from mailflow.apps import MailflowConfig
from mailflow.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView, NewsLetterRecipientListView

app_name = MailflowConfig.name

urlpatterns = [
    path('mailings/', NewsLetterListView.as_view(), name='mailings_list'),
    path('mailings/create/', NewsLetterCreateView.as_view(), name='mailings_create'),
    path('mailings/<int:pk>/', NewsLetterDetailView.as_view(), name='mailings_detail'),
    path('recipients/', NewsLetterRecipientListView.as_view(), name='recipients_list')
]