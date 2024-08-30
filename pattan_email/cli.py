import json
import click
from pattan_email import constants
from commands.template import template
from pattan_email.commands.template import list_template
from sendgrid import SendGridAPIClient


@click.group('pe', invoke_without_command=True)
@click.pass_context
@click.option('--config', type=click.Path(), required=False)
def main(context, config):
    if not config:
        config = constants.CONFIG_FILES[0]  # check home dir

    with open(config, "r") as f:
        file_content = f.read()

    context.configuration = json.loads(file_content)
    context.sg_client = SendGridAPIClient(api_key=context.configuration['api_key'])


main.add_command(template)

if __name__ == "__main__":
    main()
