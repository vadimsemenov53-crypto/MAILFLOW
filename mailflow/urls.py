from django.urls import path
from mailflow.apps import MailflowConfig
from mailflow.views import RecipientListView

app_name = MailflowConfig.name

urlpatterns = [
    path('main/', RecipientListView.as_view(), name='recipient_list'),
]