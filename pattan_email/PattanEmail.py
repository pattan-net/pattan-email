from sendgrid import SendGridAPIClient
import json
from .exceptions import InvalidEmailPurpose, MailSendFailure, MissingAPIKey, InvalidPurpose


class PattanEmail:
    def __init__(self, api_key=None, purpose='transactional'):
        self.api_key = api_key
        self._purpose = purpose

        if not self.api_key:
            raise MissingAPIKey

        if self._purpose != 'transactional' or self._purpose !=  'marketing':
            raise InvalidPurpose

    def set_purpose(self, purpose):
        if purpose != 'marketing' and purpose != 'transactional':
            raise InvalidEmailPurpose
        self._purpose = purpose

    def get_purpose(self):
        return self._purpose

    def send_template_email(self, to_addr, subject, body, from_value=None, template="PATTAN_DEFAULT_TEMPLATE",
                            asm_group="pattan unsubscribe"):
        sg = SendGridAPIClient(api_key=self.api_key)
        sender = None
        sg_response = ''
        if from_value and from_value.isnumeric():
            sender_response = sg.client.senders._(from_value).get()
            if sender_response.status_code == 200:
                sender = json.loads(sender_response.body)
        if not sender:
            sender = self.senders['DEFAULT']

        if from_value and False == from_value.isnumeric():
            sender['nickname'] = None
            sender['from'] = {'email': from_value}
            sender['reply-to'] = from_value

        # For any future time when new capabilities need to be added, like attachments or categories:
        # https://github.com/sendgrid/sendgrid-python/blob/main/examples/mail/mail.py#L27

        dynamic_template_data = {
            'Sender_Name': sender['nickname'],
            'Sender_Address': sender['address'],
            'Sender_City': sender['city'],
            'Sender_State': sender['state'],
            'Sender_Zip': sender['zip'],
            'Message_Body': body,
            'Subject': subject,
        }

        personalizations = []
        for to_address in to_addr:
            email, name = to_address
            personalizations.append({
                'to': [{'name': name, 'email': email}],
                'dynamic_template_data': dynamic_template_data,
            })

        from_email = {'email': sender['from']['email']}
        if sender['nickname']:
            from_email['name'] = sender['nickname']

        ip_pool_name = "Pattan_Marketing" if self._purpose == "marketing" else "pattan_transactional"

        asm = {
            'group_id': self.unsubscribe_groups[asm_group]['group_id'],
            'groups_to_display': [
                self.unsubscribe_groups['pattan unsubscribe']['group_id'],
                self.unsubscribe_groups['SendGrid Tech Test Group']['group_id']
            ]
        }

        template_id = self.templates[template]['sendgrid_template_id']

        message = {
            'asm': asm,
            'from': from_email,
            'ip_pool_name': ip_pool_name,
            'template_id': template_id,
            'personalizations': personalizations
        }

        try:
            sg_response = sg.client.mail.send.post(request_body=message)
        except Exception as e:
            raise MailSendFailure
        return sg_response

    templates = {
        "PATTAN_DEFAULT_TEMPLATE":
            {
                "sendgrid_template_id": "d-3890a147fac341c187cc424b1b595c4c",
            },
    }

    unsubscribe_groups = {
        'SendGrid Tech Test Group': {
            'group_id': 31335
        },
        'pattan unsubscribe': {
            'group_id': 32801
        }
    }

    senders = {
        "DEFAULT": {
            'from': {'email': 'no-reply@pattan.net'},
            'nickname': 'no-reply@pattan.net',
            'reply_to': 'no-reply@pattan.net',
            'address': '6340 Flank Drive',
            'city': 'Harrisburg',
            'state': 'Pennsylvania',
            'zip': '17112'
        }

    }
