from django.test import TestCase
import os
from pattan_email.PattanEmail import PattanEmail
from dotenv import load_dotenv

load_dotenv('../.env')

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')


def test_send_personalized_template_email():
    send_grid_template_id = 'd-66c5cd0a14224c4c9e3d52ac840486ff'
    personalization_list = []

    dynamic_template_data = {
        'Username': 'Anthony Rizzo',
        'Survey_Title': 'this is not a survey',
        'Subject': 'Greetings from the Survey team',
        'Survey_Link': 'a0a080f42e6f13b3a2df133f073095dd',
        'Signature': 'The survey team',
    }

    personalization_list.append({
        'to': [{'name': 'Anthony Rizzo', 'email': 'mweltin@pattan.net'}],
        'dynamic_template_data': dynamic_template_data,
    })

    dynamic_template_data = {
        'Username': 'Kyle Hendrix',
        'Subject': 'Greetings from the Survey team',
        'Survey_Title': 'this is not a survey',
        'Survey_Link': '<a href="forms.pattan.net/take/a0a080f42e6f13b3a2df133f073095dd">click to take survey</a>',
        'Signature': 'The survey team',
    }

    personalization_list.append({
        'to': [{'name': 'Kyle Hendrix', 'email': 'mweltin@pattan.net'}],
        'dynamic_template_data': dynamic_template_data,
    })

    emailer = PattanEmail(api_key=SENDGRID_API_KEY)
    response = emailer.send_personalized_template_email(personalization_list, send_grid_template_id)

    return response


if __name__ == "__main__":
    test_send_personalized_template_email()
