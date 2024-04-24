from django.shortcuts import render
from communications.forms import EventAllAttendeesMessageForm
from communications.PattanEmail import PattanEmail
from django.conf import settings
from eventsadmin.models import Attendee, Event
from django.shortcuts import redirect
from utils.error_codes import error_code
from django.db.models import Q
import logging
import traceback


@settings.MS_IDENTITY_WEB.login_required
def index(request, event_id):
    logger = logging.getLogger('django')
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        all_attendees_email_form = EventAllAttendeesMessageForm(request.POST)
        mailer = PattanEmail()
        mailer.purpose = 'transactional'
        to_emails = []
        if all_attendees_email_form.is_valid():
            from_address = all_attendees_email_form.cleaned_data['from_addr']
            if 15 > len(from_address) or "@pattan.net" != from_address[-11:]:
                return redirect(request.path + '?error_code=3')

            attendees = []
            if "0" == all_attendees_email_form.cleaned_data['recipients']: # all attendees
                attendees = event.attendees.all()

            if "1" == all_attendees_email_form.cleaned_data['recipients']: # presenters only
                attendees = event.presenters.all()

            if "2" == all_attendees_email_form.cleaned_data['recipients']: # missing data only
                query = Q(photo=None)
                query.add(Q(bio=None), Q.OR)
                query.add(Q(bio=""), Q.OR)
                query.add(Q(presenterevent__event=event), Q.AND)
                attendees = Attendee.objects.filter(query)

            if 0 < len(attendees):
                for attendee in attendees:
                    to_emails.append((attendee.registration_email_address, attendee.display_name))

                template = "PATTAN_DEFAULT_TEMPLATE"
                try:
                    mailer_response = mailer.send_template_email(
                        to_emails,
                        all_attendees_email_form.cleaned_data['subject'],
                        all_attendees_email_form.cleaned_data['message'],
                        all_attendees_email_form.cleaned_data['from_addr'],
                        template
                    )
                except Exception as e:
                    logger.error(traceback.format_exc())
                    return redirect(request.path + '?error_code=1&exception=true')
                # https://docs.sendgrid.com/api-reference/mail-send/mail-send
                # according to the above url 202 is the only code we need to deal with
                if mailer_response.status_code < 200 or mailer_response.status_code > 209:
                    logger.error(f"SendGrid API returned status {mailer_response.status_code}")
                    return redirect(request.path + '?error_code=1&status+error=true')
            else:
                return redirect(request.path + '?error_code=2')
        return redirect(request.path + '?error_code=0')

    error_number = request.GET.get('error_code', None)
    if error_number:
        error_number = int(error_number)
        error_string = error_code[error_number]
    else:
        error_string = ''
    all_attendees_email_form = EventAllAttendeesMessageForm()
    context = {'form': all_attendees_email_form, 'event': event, 'event_id': event.id,
               'error_number': error_number, 'error_string': error_string}
    return render(request, 'communications/index.html', context)
