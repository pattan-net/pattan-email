from django.test import TestCase
import os
import json
from pattan_email.PattanEmail import PattanEmail
from dotenv import load_dotenv
from pattan_email.models import Config

load_dotenv('../../.env')

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

PATTAN_CONFIG_JSON = os.environ.get('PATTAN_CONFIG_JSON', '')
pattan_config = json.loads(os.environ.get('PATTAN_CONFIG_JSON', ''))

pass
def test_send_personalized_template_email():
    pattan_email_config = Config.model_validate_json(PATTAN_CONFIG_JSON)
    emailer = PattanEmail(pattan_email_config)
    response = emailer.send_personalized_template_email(personalization_list, send_grid_template_id)

    return response


if __name__ == "__main__":
    test_send_personalized_template_email()
