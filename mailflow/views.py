from django.shortcuts import render
from mailflow.models import NewsLetterRecipient, Message, NewsLetter, AttemptedMailing
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

# Create your views here.

class RecipientListView(ListView):
    model = NewsLetterRecipient

