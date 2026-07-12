from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View, TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from mailflow.models import AttemptedMailing, Message, NewsLetter, NewsLetterRecipient
from mailflow.forms import NewsLetterForm, NewsLetterRecipientForm, MessageForm

from mailflow.services import send_newsletter

# Create your views here.
class MainView(TemplateView):
    template_name = 'mailflow/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context["total_mailings"] = NewsLetter.objects.count()

        for newsletter in NewsLetter.objects.all():
            newsletter.update_status()

        context["active_mailings"] = NewsLetter.objects.filter(
            time_start__lte=now,
            time_stop__gte=now,
            status=NewsLetter.ST_LAUNCHED
        ).count()

        context["total_recipients"] = NewsLetterRecipient.objects.count()

        return context



class NewsLetterListView(ListView):
    model = NewsLetter


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy("mailflow:mailings_list")

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.creator = user
        newsletter.save()

        return super().form_valid(form)


class NewsLetterDetailView(DetailView):
    model = NewsLetter

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm

    def get_success_url(self):
        return reverse("mailflow:mailings_detail", args=[self.kwargs.get("pk")])


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetter
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterStartView(LoginRequiredMixin, View):

    def post(self, request, pk):
        newsletter = get_object_or_404(NewsLetter, pk=pk)
        send_newsletter(newsletter)

        return redirect('mailflow:mailings_detail', newsletter.pk)


class NewsLetterRecipientListView(ListView):
    model = NewsLetterRecipient


class NewsLetterRecipientCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetterRecipient
    form_class = NewsLetterRecipientForm
    success_url = reverse_lazy("mailflow:recipients_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.creator = user
        recipient.save()

        return super().form_valid(form)


class NewsLetterRecipientDetailView(DetailView):
    model = NewsLetterRecipient


class NewsLetterRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetterRecipient
    form_class = NewsLetterRecipientForm

    def get_success_url(self):
        return reverse("mailflow:recipients_detail", args=[self.kwargs.get("pk")])


class NewsLetterRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetterRecipient
    success_url = reverse_lazy("mailflow:recipients_list")


class MessageListView(ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailflow:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.creator = user
        message.save()

        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse("mailflow:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailflow:message_list")


class AttemptedMailingListView(ListView):
    model = AttemptedMailing


class AttemptedMailingDetailView(DetailView):
    model = AttemptedMailing


class AttemptedMailingDeleteView(DeleteView):
    model = AttemptedMailing
    success_url = reverse_lazy("mailflow:attempts_list")