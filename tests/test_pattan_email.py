"""Tests for the PattanEmail class and its configuration handling."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from click.testing import CliRunner

from cli.get_config import gc, PREFERRED_SENDER, PREFERRED_UNSUBSCRIBE_GROUP, PREFERRED_IP_POOL
from pattan_sendgrid import PattanEmail
from pattan_sendgrid.exceptions import MalformedConfiguration
from fake_sendgrid import FakeSendGridClient


def gc_output():
    """The configuration `pe gc` emits for a typical PaTTAN account."""
    client = FakeSendGridClient(
        senders=[PREFERRED_SENDER],
        ip_pools=[PREFERRED_IP_POOL],
        unsubscribe_groups=[PREFERRED_UNSUBSCRIBE_GROUP],
        templates=['PaTTAN Standard'])
    result = CliRunner().invoke(gc, [], obj={'api_key': 'SG.fake', 'sg_client': client})
    assert result.exit_code == 0, result.exception
    return result.output.strip()


class _CapturedSend:
    """Stands in for PattanEmail.sg and records the message it is handed."""

    def __init__(self):
        self.message = None
        outer = self

        class _Send:
            @staticmethod
            def post(request_body=None):
                outer.message = request_body

                class _Response:
                    status_code = 202
                return _Response()

        class _Mail:
            send = _Send()

        class _Client:
            mail = _Mail()

        self.client = _Client()


class ConfigurationTest(unittest.TestCase):
    """gc's output has to be loadable by the class it is generated for."""

    def test_gc_output_round_trips(self):
        emailer = PattanEmail(config_json=gc_output())
        self.assertEqual(list(emailer.templates), ['PaTTAN Standard'])
        self.assertIn('DEFAULT', emailer.senders)
        self.assertIn('DEFAULT', emailer.unsubscribe_groups)
        self.assertIn('DEFAULT', emailer.ip_pool)

    def test_missing_config_is_rejected(self):
        for config in (None, '', '{}', '{"api_key": "SG.fake"}'):
            with self.subTest(config=config):
                with self.assertRaises(MalformedConfiguration):
                    PattanEmail(config_json=config)

    def test_config_without_default_sender_is_rejected(self):
        config = json.loads(gc_output())
        del config['senders']['DEFAULT']
        with self.assertRaises(MalformedConfiguration):
            PattanEmail(config_json=json.dumps(config))


class SendTemplateEmailTest(unittest.TestCase):

    def setUp(self):
        self.emailer = PattanEmail(config_json=gc_output())
        self.captured = _CapturedSend()
        self.emailer.sg = self.captured

    def test_email_template_is_required(self):
        """Omitting the template fails at the call site, not deep in the send."""
        with self.assertRaises(TypeError):
            self.emailer.send_template_email('bob@example.com')
        with self.assertRaises(TypeError):
            self.emailer.send_template_email(
                'bob@example.com', dynamic_template_data={'first_name': 'Bob'})

    def test_sends_with_the_named_template(self):
        response = self.emailer.send_template_email(
            'bob@example.com', 'PaTTAN Standard', {'first_name': 'Bob'})
        self.assertEqual(response.status_code, 202)
        message = self.captured.message
        self.assertEqual(message['template_id'], 'd-1')
        self.assertEqual(message['ip_pool_name'], PREFERRED_IP_POOL)
        self.assertEqual(
            message['personalizations'][0]['dynamic_template_data'],
            {'first_name': 'Bob'})

    def test_string_recipient_is_expanded(self):
        self.emailer.send_template_email('bob@example.com', 'PaTTAN Standard')
        recipients = self.captured.message['personalizations'][0]['to']
        self.assertEqual(recipients, [{'name': 'bob@example.com',
                                       'email': 'bob@example.com'}])

    def test_unknown_template_name_is_rejected(self):
        with self.assertRaises(KeyError):
            self.emailer.send_template_email('bob@example.com', 'No Such Template')


if __name__ == '__main__':
    unittest.main()
