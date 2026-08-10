from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import render


class BroadcastEmailForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 8}))


class BroadcastEmailAdminMixin:
    """Adds a "Email selected" admin action that shows an intermediate
    compose page, then sends one individual email per recipient (never a
    shared To:/CC: — that would leak every recipient's address to the
    others) over a single reused SMTP connection.

    Subclasses just implement `get_broadcast_email(obj)` to say where the
    address lives on that row — e.g. `obj.email` for User,
    `obj.student.email` for Waitlist.
    """

    def get_broadcast_email(self, obj):
        raise NotImplementedError("Set get_broadcast_email() on this ModelAdmin")

    @admin.action(description="Email selected")
    def broadcast_email(self, request, queryset):
        form = None

        if "apply" in request.POST:
            form = BroadcastEmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]
                recipients = sorted(
                    {email for obj in queryset if (email := self.get_broadcast_email(obj))}
                )

                connection = get_connection()
                sent = 0
                connection.open()
                try:
                    for email in recipients:
                        EmailMessage(subject, message, to=[email], connection=connection).send(
                            fail_silently=True
                        )
                        sent += 1
                finally:
                    connection.close()

                self.message_user(request, f"Sent to {sent} recipient(s).")
                return None

        if form is None:
            form = BroadcastEmailForm()

        recipients_preview = sorted(
            {email for obj in queryset if (email := self.get_broadcast_email(obj))}
        )

        return render(
            request,
            "admin/broadcast_email_form.html",
            {
                "recipients": recipients_preview,
                "form": form,
                "queryset": queryset,
                "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
                "opts": self.model._meta,
                "title": "Send email to selected",
            },
        )
