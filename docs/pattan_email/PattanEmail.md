Module pattan_email.PattanEmail
===============================

Classes
-------

`PattanEmail(unsubscribe_groups, senders, templates, api_key=None, purpose='transactional')`
:   

    ### Methods

    `get_purpose(self)`
    :

    `send_personalized_template_email(self, personalization_list, template_id, from_value='no-reply@pattan.net')`
    :   This function should be used when the email is unique for each recipient.
        :param personalization_list: contains a sender tuple and all the parameters in th sendgrid template.
        :return:

    `send_template_email(self, to_addr, subject, body, from_value=None, template='DEFAULT_TEMPLATE', asm_group='DEFAULT_ASM')`
    :   This function is good to use when the email being sent is same for each recipient.
        :param to_addr:
        :param subject:
        :param body:
        :param from_value:
        :param template:
        :param asm_group:
        :return: SendGrid client response or throws an exception

    `set_purpose(self, purpose)`
    :