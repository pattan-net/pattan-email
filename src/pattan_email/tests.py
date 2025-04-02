import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pattan_email.PattanEmail import PattanEmail
from dotenv import load_dotenv
from pattan_email.models import Config

load_dotenv('../../.env')


PATTAN_EMAIL_CONFIG_JSON = os.environ.get('PATTAN_EMAIL_CONFIG_JSON', '')

def test_send_personalized_template_email():

    pattan_email_config = Config.model_validate_json(PATTAN_EMAIL_CONFIG_JSON)
    emailer = PattanEmail(pattan_email_config)
    subject_body_str = 'pattan email package test of send template email using defaults'
    to_addr = [{'name':'markus weltin', 'email':'mweltin@pattan.net'}]
    response = emailer.send_template_email(to_addr, subject_body_str, subject_body_str)

    # personalization_list = [] # https://www.twilio.com/docs/sendgrid/for-developers/sending-email/personalizations
    # response = emailer.send_personalized_template_email(personalization_list)

    return response


def apiexampletest():
    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python


    message = Mail(
        from_email='no-reply@pattan.net',
        to_emails='mweltin@pattan.net',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test_send_personalized_template_email()
