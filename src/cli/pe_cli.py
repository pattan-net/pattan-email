import os
import click
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
from cli.get_config import gc, gs, ga, gt

load_dotenv('../../.env')

@click.group()
@click.pass_context
def pe_cli(ctx):
    """CLI interface into the sendgrid backend to run export SENDGRID_API_KEY environment variable"""
    sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    ctx.obj = {'sg_client': sg.client}



pe_cli.add_command(gc)
pe_cli.add_command(gs)
pe_cli.add_command(ga)
pe_cli.add_command(gt)


if __name__ == '__main__':
    pe_cli()