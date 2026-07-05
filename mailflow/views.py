from django.shortcuts import render
from mailflow.models import NewsLetterRecipient, Message, NewsLetter, AttemptedMailing
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

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
        return reverse('mailflow:mailings_detail', args=[self.kwargs.get('pk')])


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterRecipientListView(ListView):
    model = NewsLetterRecipient
