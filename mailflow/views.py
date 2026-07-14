from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone

from mailflow.models import AttemptedMailing, Message, NewsLetter, NewsLetterRecipient
from mailflow.forms import NewsLetterForm, NewsLetterRecipientForm, MessageForm

from mailflow.services import send_newsletter

# Create your views here.
class MainView(TemplateView):
    template_name = 'mailflow/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context["total_mailings"] = 0
            context["active_mailings"] = 0
            context["total_recipients"] = 0
            return context

        user = self.request.user
        newsletters = NewsLetter.objects.filter(creator=user)

        context["total_mailings"] = newsletters.count()

        for newsletter in newsletters:
            newsletter.update_status()

        context["active_mailings"] = AttemptedMailing.objects.filter(
            newsletter__creator=user,
            status=AttemptedMailing.ST_SUCCESS
        ).count()

        context["total_recipients"] = NewsLetterRecipient.objects.filter(
            creator=user,
        ).count()

        return context



class NewsLetterListView(ListView):
    model = NewsLetter

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_superuser:
            return NewsLetter.objects.all()

        return NewsLetter.objects.filter(creator=self.request.user)


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

    def get_form(self, form_class=NewsLetterForm):
        form = super().get_form(form_class)

        form.fields['recipients'].queryset = (
            NewsLetterRecipient.objects.filter(
                creator=self.request.user
            )
        )

        return form


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

    def get_form(self, form_class=NewsLetterForm):
        form = super().get_form(form_class)

        form.fields['recipients'].queryset = (
            NewsLetterRecipient.objects.filter(
                creator=self.request.user
            )
        )

        return form


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetter
    success_url = reverse_lazy("mailflow:mailings_list")


class NewsLetterStartView(LoginRequiredMixin, View):

    def post(self, request, pk):
        newsletter = get_object_or_404(NewsLetter, pk=pk)
        send_newsletter(newsletter)

        return redirect('mailflow:mailings_detail', newsletter.pk)


class NewsLetterStopView(LoginRequiredMixin, View):

    def post(self, request, pk):
        newsletter = get_object_or_404(NewsLetter, pk=pk)

        if not (request.user.is_manager or newsletter.creator == self.request.user):
            raise PermissionDenied

        if newsletter.status == NewsLetter.ST_COMPLETED:
            raise ValidationError("Рассылка уже завершена")

        newsletter.time_stop = timezone.now()
        newsletter.status = NewsLetter.ST_COMPLETED

        newsletter.save(
            update_fields=["time_stop", "status"]
        )

        return redirect("mailflow:mailings_list")



class NewsLetterRecipientListView(ListView):
    model = NewsLetterRecipient

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_superuser:
            return NewsLetterRecipient.objects.all()

        return NewsLetterRecipient.objects.filter(creator=self.request.user)


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

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_superuser:
            return Message.objects.all()

        return Message.objects.filter(creator=self.request.user)


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


class AttemptedMailingListView(LoginRequiredMixin, ListView):
    model = AttemptedMailing

    def get_queryset(self):
        if self.request.user.is_manager or self.request.user.is_superuser:
            return AttemptedMailing.objects.all()

        return AttemptedMailing.objects.filter(newsletter__creator=self.request.user)


class AttemptedMailingDetailView(LoginRequiredMixin, DetailView):
    model = AttemptedMailing


class AttemptedMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = AttemptedMailing
    success_url = reverse_lazy("mailflow:attempts_list")