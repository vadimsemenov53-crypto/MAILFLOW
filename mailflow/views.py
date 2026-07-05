from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from mailflow.models import AttemptedMailing, Message, NewsLetter, NewsLetterRecipient

# Create your views here.


class NewsLetterListView(ListView):
    model = NewsLetter


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    fields = (
        "name",
        "time_start",
        "time_stop",
        "message",
        "recipients",
    )
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterDetailView(DetailView):
    model = NewsLetter

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    fields = (
        "name",
        "time_start",
        "time_stop",
        "message",
        "recipients",
    )

    def get_success_url(self):
        return reverse("mailflow:mailings_detail", args=[self.kwargs.get("pk")])


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterRecipientListView(ListView):
    model = NewsLetterRecipient


class NewsLetterRecipientCreateView(CreateView):
    model = NewsLetterRecipient
    fields = (
        "email",
        "first_name",
        "last_name",
        "surname",
        "comment",
    )
    success_url = reverse_lazy("mailflow:recipients_list")


class NewsLetterRecipientDetailView(DetailView):
    model = NewsLetterRecipient


class NewsLetterRecipientUpdateView(UpdateView):
    model = NewsLetterRecipient
    fields = (
        "email",
        "first_name",
        "last_name",
        "surname",
        "comment",
    )

    def get_success_url(self):
        return reverse("mailflow:recipients_detail", args=[self.kwargs.get("pk")])


class NewsLetterRecipientDeleteView(DeleteView):
    model = NewsLetterRecipient
    success_url = reverse_lazy("mailflow:recipients_list")


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = (
        "subject",
        "body",
    )
    success_url = reverse_lazy("mailflow:message_list")


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = (
        "subject",
        "body",
    )

    def get_success_url(self):
        return reverse("mailflow:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailflow:message_list")
