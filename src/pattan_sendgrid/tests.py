import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pattan_sendgrid import PattanEmail
from dotenv import load_dotenv


load_dotenv('../../.env')


PATTAN_EMAIL_CONFIG_JSON = os.environ.get('PATTAN_SENDGRID_CONFIG', None)

def test_send_personalized_template_email():

    emailer = PattanEmail(PATTAN_EMAIL_CONFIG_JSON)
    to_addr = [{'name':'markus weltin', 'email':'mweltin@pattan.net'}]
    body = "body of test email"
    subject = "subject of test email"
    dynamic_template_data = {
        'Sender_Name': emailer.senders['DEFAULT'].nickname,
        'Sender_Address': emailer.senders['DEFAULT'].address,
        'Sender_City': emailer.senders['DEFAULT'].city,
        'Sender_State': emailer.senders['DEFAULT'].state,
        'Sender_Zip': emailer.senders['DEFAULT'].zip,
        'Message_Body': body,
        'Subject': subject,
    }

    response = emailer.send_template_email(to_addr, dynamic_template_data )

    # personalization_list = [] # https://www.twilio.com/docs/sendgrid/for-developers/sending-email/personalizations
    # response = emailer.send_personalized_template_email(personalization_list)

    print(response.status_code)
    print(response.body)
    print(response.headers)
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


def api_test():
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.ips.pools.get()
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == "__main__":
    test_send_personalized_template_email()
    # apiexampletest()
    # api_test()