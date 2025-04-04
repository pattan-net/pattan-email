from sendgrid import SendGridAPIClient
from .exceptions import MailSendFailure, MalformedConfiguration
from pattan_email.models import Config

class PattanEmail:
    def __init__(self, config_json=None ):
        if not config_json:
            raise MalformedConfiguration
        try:
            # pydantic validator makes sure each property is defined and default value
            self.config = Config.model_validate_json(config_json)
        except Exception as e:
            raise MalformedConfiguration

        self.api_key = self.config.api_key
        self.ip_pool = self.config.ip_pools
        self.unsubscribe_groups = self.config.unsubscribe_groups
        self.senders = self.config.senders
        self.templates = self.config.email_templates
        self.sg = SendGridAPIClient(api_key=self.api_key)



    def send_template_email(self, to_addr, dynamic_template_data=None,
                            sender='DEFAULT', email_template="DEFAULT", asm_group="DEFAULT", ip_pool="DEFAULT"):
        '''
        This function is good to use when the same email being sent to one or more recipients.
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
            "ip_pool_name": self.ip_pool[ip_pool].name,
        }
        try:
            sg_response = self.sg.client.mail.send.post(request_body=message)
        except Exception as e:
            raise MailSendFailure
        return sg_response
