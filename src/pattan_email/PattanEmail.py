from sendgrid import SendGridAPIClient
import json
from .exceptions import MailSendFailure, MissingAPIKey, InvalidPurpose


class PattanEmail:
    def __init__(self, unsubscribe_groups, senders, templates, api_key=None, purpose='transactional'):
        self.api_key = api_key
        self._purpose = purpose
        self.sg = SendGridAPIClient(api_key=self.api_key)
        self.unsubscribe_groups = unsubscribe_groups
        self.senders = senders
        self.templates = templates
        # self.unsubscribe_groups = {
        #     'SendGrid Tech Test Group': {
        #         'group_id': 31335
        #     },
        #     'pattan unsubscribe': {
        #         'group_id': 32801
        #     }
        # }
        # self.senders = {
        #     "DEFAULT": {
        #         'from': {'email': 'no-reply@pattan.net'},
        #         'nickname': 'no-reply@pattan.net',
        #         'reply_to': 'no-reply@pattan.net',
        #         'address': '6340 Flank Drive',
        #         'city': 'Harrisburg',
        #         'state': 'Pennsylvania',
        #         'zip': '17112'
        #     }
        # }
        #
        # self.templates = {
        #     "PATTAN_DEFAULT_TEMPLATE": {"sendgrid_template_id": "d-3890a147fac341c187cc424b1b595c4c", },
        #     "SURVEY_CONFIRMATION": {"sendgrid_template_id": "d-eea0f32d9ef143f48160100c363281af", },
        #     "SURVEY_REQUEST": {"sendgrid_template_id": "d-66c5cd0a14224c4c9e3d52ac840486ff", },
        # }

        if not self.api_key:
            raise MissingAPIKey

        if self._purpose != 'transactional' and self._purpose != 'marketing':
            raise InvalidPurpose

    def set_purpose(self, purpose):
        if purpose != 'marketing' and purpose != 'transactional':
            raise InvalidPurpose
        self._purpose = purpose

    def get_purpose(self):
        return self._purpose

    def send_template_email(self, to_addr, subject, body, from_value=None, template="DEFAULT_TEMPLATE",
                            asm_group="DEFAULT_ASM"):
        '''
        This function is good to use when the email being sent is same for each recipient.
        :param to_addr:
        :param subject:
        :param body:
        :param from_value:
        :param template:
        :param asm_group:
        :return: SendGrid client response or throws an exception
        '''

        sender = None
        sg_response = ''
        if from_value and from_value.isnumeric():
            sender_response = self.sg.client.senders._(from_value).get()
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

        ip_pool_name = "marketing" if self._purpose == "marketing" else "transactional"

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
            sg_response = self.sg.client.mail.send.post(request_body=message)
        except Exception as e:
            raise MailSendFailure
        return sg_response


    def send_personalized_template_email(self, personalization_list, template_id, from_value='no-reply@pattan.net'):
        """
        This function should be used when the email is unique for each recipient.
        :param personalization_list: contains a sender tuple and all the parameters in th sendgrid template.
        :return:
        """
        sender = self.senders['DEFAULT']
        from_email = {'email': sender['from']['email'], 'name': sender['nickname']}

        ip_pool_name = "Pattan_Marketing" if self._purpose == "marketing" else "pattan_transactional"

        asm = {
            'group_id': self.unsubscribe_groups['pattan unsubscribe']['group_id'],
            'groups_to_display': [
                self.unsubscribe_groups['pattan unsubscribe']['group_id'],
                self.unsubscribe_groups['SendGrid Tech Test Group']['group_id']
            ]
        }

        message = {
            'asm': asm,
            'from': from_email,
            'ip_pool_name': ip_pool_name,
            'template_id': template_id,
            'personalizations': personalization_list
        }

        try:
            sg_response = self.sg.client.mail.send.post(request_body=message)
        except Exception as e:
            raise MailSendFailure
        return sg_response
