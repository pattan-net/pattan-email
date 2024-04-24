from django import forms
from sendgrid import SendGridAPIClient
from django.conf import settings
import json


class EventAllAttendeesMessageForm(forms.Form):
    recipients = forms.ChoiceField(choices=[])
    from_addr = forms.EmailField()
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "tinymce event-form-full-width"}))
    # message is not required because chrome's validator errors out on tinyMCE fields that are required
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "tinymce event-form-full-width"}), required=False)

    def __init__(self, *args, **kwargs):
        super(EventAllAttendeesMessageForm, self).__init__(*args, **kwargs)
        self.fields['from_addr'].label = 'From address'

        choices = (
            (0, "All attendees"),
            (1, "Presenters only"),
            (2, "Only presenters missing required data"),
        )
        self.fields['recipients'].choices = choices
