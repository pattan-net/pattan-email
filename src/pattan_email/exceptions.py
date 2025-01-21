class InvalidEmailPurpose(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "InvalidEmailPurpose, {0} ".format(self.message)
        else:
            return "InvalidEmailPurpose valid values include 'transactional' or 'marketing"


class MailSendFailure(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "MailSendFailure, {0} ".format(self.message)
        else:
            return "MailSendFailure attempts to send email failed"


class MissingAPIKey(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "MissingAPIKey, {0} ".format(self.message)
        else:
            return "MissingAPIKey a sendgrid API key must be provided to create an instance this class"


class InvalidPurpose(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "InvalidPurpose, {0} ".format(self.message)
        else:
            return "InvalidPurpose value must be either 'transactional' or 'marketing'"
