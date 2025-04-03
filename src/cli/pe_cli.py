# cli.py
import os
import click
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv

load_dotenv('../../.env')

@click.command()
@click.option('--name', default='World', help='Name to greet')
def pe_cli(name):
    """Simple program that greets NAME."""
    click.echo(f'Hello, {name}!')
    sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))


if __name__ == '__main__':
    pe_cli()