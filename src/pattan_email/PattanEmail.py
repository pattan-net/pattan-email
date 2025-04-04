from sendgrid import SendGridAPIClient
import json
from .exceptions import MailSendFailure, MissingAPIKey, MalformedConfiguration


class PattanEmail:
    def __init__(self, config=None ):
        if not config:
            raise MalformedConfiguration

        if not config.api_key:
            raise MissingAPIKey

        self.api_key = config.api_key
        self.ip_pool = config.ip_pools["DEFAULT"].name
        self.unsubscribe_groups = config.unsubscribe_groups
        self.senders = config.senders
        self.templates = config.email_templates
        self.sg = SendGridAPIClient(api_key=self.api_key)



    def send_template_email(self, to_addr, dynamic_template_data=None,
                            sender='DEFAULT', email_template="DEFAULT", asm_group="DEFAULT", ip_pool_key="DEFAULT"):
        '''
        This function is good to use when the email being sent is same for each recipient.
        :param email_template:
        :param sender:
        :param dynamic_template_data:
        :param to_addr: email address or list of "address" dicts e.g. [{'name':'bob', 'email':'bob@example.com'}]
        :param subject:
        :param body:
        :param asm_group:
        :return: SendGrid client response or throws an exception
        '''

        if sender not in self.senders.keys():
            raise MalformedConfiguration('Assigned sender is not defined in your configuration')

        sender = self.senders[sender]

        # the to_addr can be a list of just a string of an email address.
        if isinstance(to_addr, str):
            to_addr = [{'name': to_addr, 'email': to_addr}]

        personalizations = []
        personalizations.append({
            'to': to_addr,
            'dynamic_template_data': dynamic_template_data
        })

        from_email = {'email': sender.from_address.email}
        if sender.nickname:
            from_email['name'] = sender.nickname

        asm = {
            'group_id': self.unsubscribe_groups[asm_group].id,
            'groups_to_display': [
                self.unsubscribe_groups[asm_group].id
            ]
        }

        template_id = self.templates[email_template].id

        message = {
            "from": from_email,
            "personalizations": personalizations,
            "template_id": template_id,
            "asm": asm,
            "ip_pool_name": self.ip_pool,
        }
        try:
            sg_response = self.sg.client.mail.send.post(request_body=message)
        except Exception as e:
            raise MailSendFailure
        return sg_response

    def send_personalized_template_email(self, personalization_list=None, template='DEFAULT', sender='DEFAULT'):
        """
        This function should be used when the email is unique for each recipient.
        :param template:
        :param sender:
        :param template_id:
        :param personalization_list: contains a sender tuple and all the parameters in th sendgrid template.
        :return:
        """
        if personalization_list is None:
            raise MalformedConfiguration('personalization_list can not be left blank, it defines who is being sent an email')

        sender = self.senders[sender]
        template_id = self.templates[template]['sendgrid_template_id']

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
