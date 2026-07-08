from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from mailflow.models import AttemptedMailing, Message, NewsLetter, NewsLetterRecipient
from mailflow.forms import NewsLetterForm, NewsLetterRecipientForm, MessageForm

from mailflow.services import send_newsletter

# Create your views here.


class NewsLetterListView(ListView):
    model = NewsLetter


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterDetailView(DetailView):
    model = NewsLetter

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm

    def get_success_url(self):
        return reverse("mailflow:mailings_detail", args=[self.kwargs.get("pk")])


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterStartView(View):

    def post(self, request, pk):
        newsletter = get_object_or_404(NewsLetter, pk=pk)
        send_newsletter(newsletter)

        return redirect('mailflow:mailings_detail', newsletter.pk)


class NewsLetterRecipientListView(ListView):
    model = NewsLetterRecipient


class NewsLetterRecipientCreateView(CreateView):
    model = NewsLetterRecipient
    form_class = NewsLetterRecipientForm
    success_url = reverse_lazy("mailflow:recipients_list")


class NewsLetterRecipientDetailView(DetailView):
    model = NewsLetterRecipient


class NewsLetterRecipientUpdateView(UpdateView):
    model = NewsLetterRecipient
    form_class = NewsLetterRecipientForm

    def get_success_url(self):
        return reverse("mailflow:recipients_detail", args=[self.kwargs.get("pk")])


class NewsLetterRecipientDeleteView(DeleteView):
    model = NewsLetterRecipient
    success_url = reverse_lazy("mailflow:recipients_list")


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailflow:message_list")


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse("mailflow:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailflow:message_list")


class AttemptedMailingListView(ListView):
    model = AttemptedMailing


class AttemptedMailingDetailView(DetailView):
    model = AttemptedMailing


class AttemptedMailingDeleteView(DeleteView):
    model = AttemptedMailing
    success_url = reverse_lazy("mailflow:attempts_list")