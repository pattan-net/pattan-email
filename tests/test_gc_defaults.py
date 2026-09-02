"""Tests for how `pe gc` picks the DEFAULT entry in each config section.

The precedence is: the value given on the command line, then PaTTAN's preferred
name, then the first item the SendGrid account returns.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from click.testing import CliRunner

from cli.get_config import (
    gc,
    PREFERRED_SENDER,
    PREFERRED_IP_POOL,
    PREFERRED_UNSUBSCRIBE_GROUP,
)
from fake_sendgrid import FakeSendGridClient


def run_gc(client, *args):
    """Invoke gc against a fake client and return its parsed JSON output."""
    result = CliRunner().invoke(
        gc, list(args), obj={'api_key': 'SG.fake', 'sg_client': client})
    if result.exit_code != 0:
        raise AssertionError(
            f'gc exited {result.exit_code}: {result.exception!r}')
    return json.loads(result.output)


def run_gc_expecting_failure(client, *args):
    """Invoke gc against a fake client and return the failed click result."""
    result = CliRunner().invoke(
        gc, list(args), obj={'api_key': 'SG.fake', 'sg_client': client})
    if result.exit_code == 0:
        raise AssertionError(f'gc unexpectedly succeeded: {result.output}')
    return result


def fully_populated(**overrides):
    """A client holding the preferred name plus another one in every section."""
    kwargs = {
        'senders': [PREFERRED_SENDER, 'marketing@PaTTAN'],
        'ip_pools': [PREFERRED_IP_POOL, 'Pattan_Bulk'],
        'unsubscribe_groups': [PREFERRED_UNSUBSCRIBE_GROUP, 'Tech Test Group'],
        'templates': ['PaTTAN Standard'],
    }
    kwargs.update(overrides)
    return FakeSendGridClient(**kwargs)


class PreferredDefaultsTest(unittest.TestCase):
    """The preferred name wins when no option is given on the command line."""

    def test_preferred_names_are_used(self):
        config = run_gc(fully_populated())
        self.assertEqual(config['senders']['DEFAULT']['nickname'], PREFERRED_SENDER)
        self.assertEqual(config['ip_pools']['DEFAULT']['name'], PREFERRED_IP_POOL)
        self.assertEqual(
            config['unsubscribe_groups']['DEFAULT'],
            config['unsubscribe_groups'][PREFERRED_UNSUBSCRIBE_GROUP])

    def test_preferred_names_win_over_earlier_entries(self):
        """Order must not decide it: the preferred name is listed last here."""
        client = fully_populated(
            senders=['marketing@PaTTAN', PREFERRED_SENDER],
            ip_pools=['Pattan_Bulk', PREFERRED_IP_POOL],
            unsubscribe_groups=['Tech Test Group', PREFERRED_UNSUBSCRIBE_GROUP])
        config = run_gc(client)
        self.assertEqual(config['senders']['DEFAULT']['nickname'], PREFERRED_SENDER)
        self.assertEqual(config['ip_pools']['DEFAULT']['name'], PREFERRED_IP_POOL)


class CommandLineOverrideTest(unittest.TestCase):
    """An explicit option outranks the preferred name."""

    def test_options_override_preferred_names(self):
        config = run_gc(
            fully_populated(),
            '--default-sender', 'marketing@PaTTAN',
            '--default-ip-pool', 'Pattan_Bulk',
            '--default-unsubscribe_group', 'Tech Test Group')
        self.assertEqual(config['senders']['DEFAULT']['nickname'], 'marketing@PaTTAN')
        self.assertEqual(config['ip_pools']['DEFAULT']['name'], 'Pattan_Bulk')
        self.assertEqual(config['unsubscribe_groups']['DEFAULT'],
                         config['unsubscribe_groups']['Tech Test Group'])

    def test_named_sender_must_exist(self):
        """A typo must be reported, not silently swapped for another sender."""
        result = run_gc_expecting_failure(
            fully_populated(), '--default-sender', 'typo@PaTTAN')
        self.assertEqual(result.exit_code, 2)
        self.assertIn('typo@PaTTAN', result.output)
        self.assertIn('--default-sender', result.output)
        # the message lists what could have been used instead
        self.assertIn(PREFERRED_SENDER, result.output)

    def test_named_ip_pool_must_exist(self):
        result = run_gc_expecting_failure(
            fully_populated(), '--default-ip-pool', 'No_Such_Pool')
        self.assertEqual(result.exit_code, 2)
        self.assertIn('No_Such_Pool', result.output)
        self.assertIn('--default-ip-pool', result.output)

    def test_named_unsubscribe_group_must_exist(self):
        result = run_gc_expecting_failure(
            fully_populated(), '--default-unsubscribe_group', 'No Such Group')
        self.assertEqual(result.exit_code, 2)
        self.assertIn('No Such Group', result.output)
        self.assertIn('--default-unsubscribe_group', result.output)

    def test_named_sender_is_rejected_on_an_empty_account(self):
        """Asking for a sender when the account has none is still an error."""
        result = run_gc_expecting_failure(
            FakeSendGridClient(), '--default-sender', PREFERRED_SENDER)
        self.assertEqual(result.exit_code, 2)
        self.assertIn('none', result.output)

    def test_nothing_is_written_when_a_name_is_rejected(self):
        """gc must not emit a half-built config alongside the error."""
        result = run_gc_expecting_failure(
            fully_populated(), '--default-sender', 'typo@PaTTAN')
        self.assertNotIn('"api_key"', result.output)

    def test_error_goes_to_stderr(self):
        """The README pipes gc to a file, so stdout has to stay clean."""
        result = run_gc_expecting_failure(
            fully_populated(), '--default-sender', 'typo@PaTTAN')
        self.assertEqual(result.stdout, '')
        self.assertIn('typo@PaTTAN', result.stderr)


class MissingPreferredNamesTest(unittest.TestCase):
    """Accounts without PaTTAN's preferred names fall back to the first item."""

    def test_falls_back_to_first_found(self):
        client = FakeSendGridClient(
            senders=['marketing@PaTTAN', 'events@PaTTAN'],
            ip_pools=['Pattan_Bulk', 'Other_Pool'],
            unsubscribe_groups=['Tech Test Group', 'Other Group'],
            templates=['PaTTAN Standard'])
        config = run_gc(client)
        self.assertEqual(config['senders']['DEFAULT']['nickname'], 'marketing@PaTTAN')
        self.assertEqual(config['ip_pools']['DEFAULT']['name'], 'Pattan_Bulk')
        self.assertEqual(config['unsubscribe_groups']['DEFAULT'],
                         config['unsubscribe_groups']['Tech Test Group'])

    def test_partially_matching_account(self):
        """Each section is decided on its own."""
        client = FakeSendGridClient(
            senders=[PREFERRED_SENDER],
            ip_pools=['Pattan_Bulk'],
            unsubscribe_groups=[PREFERRED_UNSUBSCRIBE_GROUP],
            templates=['PaTTAN Standard'])
        config = run_gc(client)
        self.assertEqual(config['senders']['DEFAULT']['nickname'], PREFERRED_SENDER)
        self.assertEqual(config['ip_pools']['DEFAULT']['name'], 'Pattan_Bulk')


class EmptyAccountTest(unittest.TestCase):
    """An account with nothing in it must not crash gc."""

    def test_empty_sections_produce_no_default(self):
        config = run_gc(FakeSendGridClient())
        for section in ('senders', 'ip_pools', 'unsubscribe_groups', 'email_templates'):
            self.assertEqual(config[section], {}, section)

    def test_empty_single_section(self):
        client = FakeSendGridClient(
            senders=[PREFERRED_SENDER], ip_pools=[], unsubscribe_groups=[])
        config = run_gc(client)
        self.assertEqual(config['senders']['DEFAULT']['nickname'], PREFERRED_SENDER)
        self.assertEqual(config['ip_pools'], {})


class TemplateSectionTest(unittest.TestCase):
    """Templates get no DEFAULT; callers name the template they want."""

    def test_no_default_template(self):
        config = run_gc(fully_populated(templates=['PaTTAN Standard', 'PaTTAN Alert']))
        self.assertNotIn('DEFAULT', config['email_templates'])
        self.assertEqual(sorted(config['email_templates']),
                         ['PaTTAN Alert', 'PaTTAN Standard'])

    def test_template_variables_are_collected(self):
        config = run_gc(fully_populated(templates=['PaTTAN Standard']))
        variables = config['email_templates']['PaTTAN Standard']['variables']
        self.assertIn('first_name', variables)
        self.assertIn('topic', variables)


class ApiKeyTest(unittest.TestCase):

    def test_api_key_is_passed_through(self):
        self.assertEqual(run_gc(fully_populated())['api_key'], 'SG.fake')


if __name__ == '__main__':
    unittest.main()
