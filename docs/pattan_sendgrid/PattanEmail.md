Module pattan_sendgrid.PattanEmail
==================================

Classes
-------

`PattanEmail(config_json=None)`
:   Useful SendGrid API abstraction for sending emails.
    It includes a command line interface to construct the configuration file by querying the SendGrid API directly.

    ### Methods

    `send_personalized_template_email(self, personalization_list, template_id, sender='DEFAULT', asm_group='DEFAULT', ip_pool='DEFAULT')`
    :   This function should be used when the email is unique for each recipient.
        :param personalization_list: contains a sender tuple and all the parameters in th sendgrid template.
        :return:

    `send_template_email(self, to_addr, dynamic_template_data=None, sender='DEFAULT', email_template='DEFAULT', asm_group='DEFAULT', ip_pool='DEFAULT')`
    :   Send the same email to one or more recipients.
        :param to_addr: email address dict or list of address dicts e.g. [{'name':'bob', 'email':'bob@example.com'}]
        :param dynamic_template_data: dict that defines all the variables used in the selected email_template
        :param email_template: string Name of the template you want to use e.g. "PaTTAN Standard Template"
        :param sender: string Name of the sender email address e.g. "no-reply@PaTTAN"
        :param asm_group: string Name of the asm group (a.k.a. unsubscribe group)  e.g. "SendGrid Tech Test Group"
        :param ip_pool: : string Name of the ip_pool e.g. "Pattan_Transactional"
        :return: SendGrid client response or throws an exception