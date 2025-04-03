import os
import click
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
from .get_config import gc

load_dotenv('../../.env')

@click.group()
def pe_cli():
    """CLI interface into the sendgrid backend"""
    sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))



pe_cli.add_command(gc)


if __name__ == '__main__':
    pe_cli()